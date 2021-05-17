from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.detail import SingleObjectMixin


class FormsMixin(ContextMixin):
    """ Provide a way to show and handle multiple forms in a request. """

    success_url = None
    success_urls = {}
    form_classes = {}

    def get_initial(self, form_key):
        """
        Return the initial data to use for a form on this view for a particular form key.
            Implement <form_key>_initial or get_<form_key>_initial() to specify initial data for individual forms.
        """
        initial_attr = f"{form_key}_initial"
        if hasattr(self, initial_attr):
            return getattr(self, initial_attr)

        initial_method = f"get_{form_key}_initial"
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()

        return {}

    def get_form_classes(self):
        """Return the form classes to use."""
        return {
            **self.form_classes
        }

    def get_form_class(self, form_key):
        """Return the form class to use for a particular form key."""
        return self.get_form_classes()[form_key]

    def get_form(self, form_key):
        """
        Return an instance of the form to be used in this view for a particular form key.
            Implement get_<form_key> to override the default form instantiation.
        """
        form_method = f"get_{form_key}"
        if hasattr(self, form_method):
            return getattr(self, form_method)()

        form_class = self.get_form_class(form_key)
        kwargs = self.get_form_kwargs(form_key)
        kwargs_method = f"get_{form_key}_kwargs"
        if hasattr(self, kwargs_method):
            kwargs.update(getattr(self, kwargs_method)())
        return form_class(**kwargs)

    def get_form_kwargs(self, form_key):
        """
        Return the keyword arguments for instantiating the form for a particular form key.
            Implement get_<form_key>_kwargs to add additional keyword arguments like instance or prefix.
        """
        kwargs = {
            "initial": {"multiform_key": form_key, **self.get_initial(form_key)},
        }
        if (
            self.request.method in ["POST", "PUT"]
            and self.request.POST["multiform_key"] == form_key
        ):
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )
        return kwargs

    def get_success_url(self, form_key):
        """
        Return the URL to redirect to after processing the valid form for a particular form key.
            Implement get_<form_key>_success_url or add form_key to specify for individual forms
        """
        success_url_method = f"get_{form_key}_success_url"
        if hasattr(self, success_url_method):
            return getattr(self, success_url_method)()
        elif form_key in self.success_urls:
            return str(self.success_urls[form_key])
        else:
            if not self.success_url:
                raise ImproperlyConfigured(
                    "No URL to redirect to. Provide a success_url."
                )
            return str(self.success_url)  # success_url may be lazy

    def form_valid(self, form, form_key):
        """
        If the form for a particular form key is valid, redirect to the supplied URL.
            Implement <form_key>_valid(self, form) to specify behavior for a single form
        """
        form_valid_method = f"{form_key}_valid"
        if hasattr(self, form_valid_method):
            return getattr(self, form_valid_method)(form)
        else:
            return HttpResponseRedirect(self.get_success_url(form_key))

    def form_invalid(self, form, form_key):
        """
        If the form for a particular form key is invalid, render the invalid form.
            Implement <form_key>_invalid(self, form) to specify behavior for a single form
        """
        form_invalid_method = f"{form_key}_invalid"
        if hasattr(self, form_invalid_method):
            return getattr(self, form_invalid_method)(form)
        else:
            return self.render_to_response(self.get_context_data(**{form_key: form}))

    def get_context_data(self, **kwargs):
        """
        Insert form classes into the current context using their key as their variable name.

        Also attaches a hidden field to every form in form classes called _key which helps direct submission
            to the appropriate form.
        """
        form_context = {}
        for form_key, form_class in self.get_form_classes().items():
            if form_key not in kwargs:
                form = self.get_form(form_key)
                form.fields["multiform_key"] = forms.CharField(widget=forms.HiddenInput())
                form_context[form_key] = form
            else:
                kwargs[form_key].fields["multiform_key"] = forms.CharField(
                    widget=forms.HiddenInput()
                )
        return super().get_context_data(**kwargs, **form_context)


class ProcessFormsView(View):
    """Render forms on GET and process a single form on POST."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate blank versions of the forms."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        The form class is chosen based on the hidden form input _key, which is
        attached with the context
        """
        try:
            form_key = request.POST["multiform_key"]
            form = self.get_form(form_key)
        except KeyError:
            return HttpResponseForbidden()
        if form.is_valid():
            return self.form_valid(form, form_key)
        else:
            return self.form_invalid(form, form_key)


class BaseFormsView(FormsMixin, ProcessFormsView):
    """A base view for displaying forms."""


class FormsView(TemplateResponseMixin, BaseFormsView):
    """A view for displaying forms and rendering a template response."""


class ObjectFormsView(SingleObjectMixin, FormsView):
    """
    A view for attaching a single object to a FormsView

    This is useful if you want to include ModelForms in your form view.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
