from rest_framework.views import APIView
from api.analyze.utils import (
    get_privacy_policy_url,
    get_site_html,
    text_from_html,
    get_fuzzy_result,
)
from rest_framework.response import Response


class AnalyzeUrlView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        url = request.GET.get("url")
        pp_url = get_privacy_policy_url(url)

        if not pp_url:
            return Response("Privacy Policy not found.", status=404)

        # Download all text from PP
        html = get_site_html(pp_url)
        privacy_policy_text = text_from_html(body=html)

        actions = ("access", "store", "sell", "disclose", "delete")
        all_actions = []
        for action in actions:
            result = get_fuzzy_result(action, text=privacy_policy_text)
            action_map = dict(
                type=action.title(),
                quote=result[0][0],
                confidence=result[0][1],
                classification=result[0][2],
            )
            all_actions.append(action_map)

        return Response({"actions": all_actions, "privacy_policy_link": pp_url})

    """
    Actions are delete store, etc
    results is a list of tuples
    (quote, classifier_result)
    """
