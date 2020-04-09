from proj.core.views import BaseView


class IndexView(BaseView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return self.template_response(
                request,
                "home.html",
                {
                    "should_display_chat_button": True,
                    "should_display_volume_button": False,
                    "user_is_active": bool(request.user.profile.activated_at),
                },
            )

        return self.template_response(request, "index.html")
