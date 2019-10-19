from rest_framework.views import APIView
from api.analyze.utils import (
    get_privacy_policy_url,
    get_site_html,
    text_from_html,
    parse_summary,
    parse_main_points,
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
        main_points = parse_main_points(text=privacy_policy_text)
        summary = parse_summary(text=privacy_policy_text)
        return Response({"main_points": main_points, "summary": summary})
