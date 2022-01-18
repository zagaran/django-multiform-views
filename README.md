# django-multiple-forms
An expansion of django's FormView to handle multiple form submissions

## How To Use
#### Install the dependency
```
pip install django-multiform-views
```
or add `django-multiform-views` to your `requirements.in` file, then run
```
pip compile
pip install -r requirements.txt
```

#### Usage
Have your view inherit from ```FormsView```.

Render `multiform_key` as a hidden input in the frontend form. This can be done manually or by 
appending `multiform_key` to the layout is using crispy forms. The key is already added to the 
form initial so only the frontend addition is needed.

Instead of the `FormView` `form_class` property, define the `form_classes` property as a dictionary of
`String`, `Form` class pairs:
```
form_classes = {
    'first_form': FirstForm,
    'second_form': SecondForm,
}
```
Alternatively you can override the `get_form_classes()` function, which by default returns the 
`form_classes` property

The package will detect which form was submitted in the view. You can perform 
individual validation for each form:
```
def first_form_valid(self, form):
    ...

def second_form_valid(self, form):
    ...
```
This same pattern is true for all form instantiation and handling methods from FormView. They can be
 defined individually for each form using the form key defined in form_classes as an infix, e.g. 
 `get_initial` becomes `get_first_form_initial` and `get_form_kwargs` becomes `get_second_form_kwargs`.

All other class properties and methods behave identically to those in Django's `FormView`

