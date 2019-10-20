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
        results = get_fuzzy_result("delete", text=privacy_policy_text)
        action_map = dict()
        action_map["type"] = "Delete"
        action_map["quote"] = results[0][0]
        action_map["confidence"] = results[0][1]
        action_map["classification"] = results[0][2]
        all_actions = [action_map]

        return Response({"actions": all_actions, "privacy_policy_link": pp_url})

    """
    Actions are delete store, etc
    results is a list of tuples
    (quote, classifier_result)
    """
