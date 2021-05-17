from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from django.views.generic.base import ContextMixin, View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin


class FormInjection(FormMixin):
    """
    FormInjection is a template class to be used with InjectionFormsViews to attach multiple forms to a single View
    """
    form_name = None

    def __init__(self, request, default_success_url=None):
        self.request = request
        self.default_success_url = default_success_url
        for attr in ["form_class", "form_name"]:
            if not getattr(self, attr):
                raise NotImplementedError(f"FormInjection must define a {attr} attribute.")

    def get_success_url(self):
        """Substitute in the default success url if there is one."""
        if not self.success_url:
            if not self.default_success_url:
                raise ImproperlyConfigured("No URL or default URL to redirect to. Provide a success_url on the form injection or the InjectionFormsView.")
            return str(self.default_success_url)
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        """This method is handled in the InjectionFormsMixin."""
        raise


class InjectionFormsMixin(ContextMixin):
    """ A better way to show and handle multiple forms in a request. """

    success_url = None
    form_injections = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.injections_map = {}
        for injection in self.get_form_injections():
            key = injection.form_name
            if key in self.injections_map:
                raise KeyError(f"Found multiple forms named {key} in InjectionFormView.")
            else:
                self.injections_map[key] = injection(self.request)

    def get_form_injections(self):
        """Return the form injections to use."""
        return self.form_injections

    def get_form(self, form_key):
        """Locate the appropriate form and call its get_form method"""

    def form_valid(self, form):
        """Locate the appropriate form and call its form_valid method."""

    def form_invalid(self):
        """Call the injection's form invalid and then rerender the forms."""

    def get_context_data(self, **kwargs):
        """
        Insert form classes into the current context using their key as their variable name.

        Also attaches a hidden field to every form in form classes called _key which helps direct submission
            to the appropriate form.
        """
        form_context = {
            form_injection.form_name: form_injection.get_form() for form_injection in self.get_form_injections()
        }
        return super().get_context_data(**kwargs, **form_context)


class ProcessInjectionFormsView(View):
    """Render injection forms on GET and process a single injection form on POST."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate blank versions of the injection forms."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate the injection form instance with the passed
        POST variables and then check if it's valid.

        The form class is chosen based on the hidden form input multiform_key, which is
        attached with the context
        """
        form_key = request.POST.get("multiform_key", None)
        if not form_key or form_key not in self.injections_map:
            return HttpResponseForbidden()
        injection = self.injections_map[form_key]
        form = injection.get_form()
        if form.is_valid():
            return injection.form_valid(form)
        else:
            return injection.form_invalid(form)


class BaseFormsView(InjectionFormsMixin, ProcessInjectionFormsView):
    """A base view for displaying forms."""


class InjectionFormsView(TemplateResponseMixin, BaseFormsView):
    """A view for displaying forms and rendering a template response."""


class ObjectInjectionFormsView(SingleObjectMixin, InjectionFormsView):
    """
    A view for attaching a single object to a InjectionFormsView

    This is useful if you want to include ModelForms in your form view.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
