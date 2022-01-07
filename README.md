# django-multiple-forms
An expansion of django's FormView to handle multiple form submissions

## How To Use
#### Install the dependency
```
pip install django-mulitform-views
```
or add `django-multiform-views` to your `requirements.in` file, then run
```
pip compile
pip install -r requirements.txt
```

#### Usage
Have your view inherit from ```FormsView```.

Append `multiform_key` to `helper.layout` in the form

Add the fields for `template_name`, `success_url`, etc as you would normally for `FormView`

Add the `form_classes` for each form you want in your view
```
form_classes = {
    'first_form': FirstForm,
    'second_form': SecondForm,
}
```
The package will detect which form was submitted in the view. You can perform 
individual validation for each form:
```
def first_form_valid(self, form):
    ...

def second_form_valid(self, form):
    ...
```

