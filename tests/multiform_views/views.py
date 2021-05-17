from multiform_views.edit import FormsView, ObjectFormsView

from .forms import JournalistForm, CommentForm


class JournalistAndCommentFormsView(FormsView):
    success_url = "/journalist/detail"

    form_classes = {
        'journalist_form': JournalistForm,
        'comment_form': CommentForm
    }

    def get_comment_form_success_url(self):
        return "/comments"


class MultipleCommentsFormsView(FormsView):
    success_urls = {
        "comment_form_1": "/comments/1",
        "comment_form_2": "/comments/2",
        "comment_form_3": "/comments/3",
    }

    form_classes = {
        'comment_form_1': CommentForm,
        'comment_form_2': CommentForm,
        'comment_form_3': CommentForm,
    }

