from rest_framework.views import APIView
from api.analyze.utils import (
    get_privacy_policy_url,
    get_site_html,
    text_from_html,
    # parse_summary,
    # parse_main_points,
    # get_classifier_result,
    get_fuzzy_result,
    # get_classifier_result
)
from urllib.parse import urlsplit
from rest_framework.response import Response


class AnalyzeUrlView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        signup_url = request.GET.get("url")
        split_url = urlsplit(signup_url)
        # Find base uri from current url, so we can search the homepage
        base_uri = f"{split_url.scheme}://{split_url.netloc}"

        # Parse out url to find privacy policy
        pp_url = get_privacy_policy_url(signup_url)
        # If not found, re-run search base_url and search for privacy policy links

        if not pp_url:
            pp_url = get_privacy_policy_url(base_uri)
            if not pp_url:
                return Response("Privacy Policy not found.")

        if "http" or "https" in pp_url:
            pp_url = f"{base_uri}{pp_url}"

        # Download all text from PP
        html = get_site_html(pp_url)
        privacy_policy_text = text_from_html(body=html)
        results = get_fuzzy_result("delete", text=privacy_policy_text)
        # summary = parse_summary(text=privacy_policy_text)
        action_map = {}
        action_map["type"] = "Delete"
        action_map["quote"] = results[0][0]
        action_map["confidence"] = results[0][1]
        action_map["classification"] = results[0][2]
        all_actions = [action_map]

        return Response({"actions" : all_actions, "privacy_policy_link" : pp_url})

    """
    Actions are delete store, etc
    results is a list of tuples
    (quote, classifier_result)
    """
