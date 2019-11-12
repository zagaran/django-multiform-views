

class FormsMixin(ContextMixin):
    """ """
    success_url = None
    success_urls = {}
    form_classes = {}

    def get_initial(self, form_key):
        initial_attr = f"{form_key}_initial"
        if hasattr(self, initial_attr):
            return getattr(self, initial_attr)
        initial_method = f"get_{form_key}_initial"
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return {}

    def get_prefix(self, form_key):
        if hasattr(self, f"{form_key}_prefix"):
            return getattr(self, f"{form_key}_prefix")
        elif hasattr(self, f"get_{form_key}_prefix"):
            return getattr(self, f"get_{form_key}_prefix")()
        else:
            return None

    def get_form_classes(self):
        return self.form_classes

    def get_form_class(self, form_key):
        return self.get_form_classes()[form_key]

    def get_form(self, form_key):
        form_class = self.get_form_class(form_key)
        kwargs = self.get_form_kwargs(form_key)
        if hasattr(self, f"get_{form_key}_kwargs"):
            kwargs.update(getattr(self, f"get_{form_key}_kwargs")())
        return form_class(**kwargs)

    def get_form_kwargs(self, form_key):
        kwargs = {
            'initial': {
                '_key': form_key,
                **self.get_initial(form_key)
            },
            'prefix': self.get_prefix(form_key)
        }
        if self.request.method in ['POST', 'PUT'] and self.request.POST['_key'] == form_key:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self, form_key):
        """Return the URL to redirect to after processing a valid form."""
        if hasattr(self, f"get_{form_key}_success_url"):
            return getattr(self, f"get_{form_key}_success_url")()
        elif form_key in self.success_urls:
            return str(self.success_urls[form_key])
        else:
            if not self.success_url:
                raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
            return str(self.success_url)  # success_url may be lazy

    def form_valid(self, form, form_key):
        if hasattr(self, f"{form_key}_valid"):
            return getattr(self, f"{form_key}_valid")(form)
        else:
            return HttpResponseRedirect(self.get_success_url(form_key))

    def form_invalid(self, form, form_key):
        if hasattr(self, f"{form_key}_invalid"):
            return getattr(self, f"{form_key}_invalid")(form)
        else:
            return self.render_to_response(self.get_context_data(**{form_key: form}))

    def get_context_data(self, **kwargs):
        form_context = {}
        for form_key, form_class in self.get_form_classes().items():
            if form_key not in kwargs:
                form = self.get_form(form_key)
                form.fields['_key'] = forms.CharField(widget=forms.HiddenInput())
                form_context[form_key] = form
            else:
                kwargs[form_key].fields['_key'] = forms.CharField(widget=forms.HiddenInput())
        return super().get_context_data(**kwargs, **form_context)


class ProcessFormsView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        if "_key" in request.POST:
            form_key = request.POST["_key"]
            form = self.get_form(form_key)
            if form.is_valid():
                return self.form_valid(form, form_key)
            else:
                return self.form_invalid(form, form_key)
        else:
            return super().post(request, *args, **kwargs)


class BaseFormsView(FormsMixin, ProcessFormsView):
    """  """


class FormsView(TemplateResponseMixin, BaseFormsView):
    """ """