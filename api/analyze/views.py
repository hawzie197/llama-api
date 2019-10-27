# [Django]
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

# [App]
from api.analyze.serializers import UrlQueryParamSerizlizer, AnalysisSerializer
from api.analyze.utils import find_privacy_policy_url, text_from_html, get_fuzzy_result

# from api.analyze.webdriver import driver
from requests_html import HTMLSession

session = HTMLSession()


class AnalyzeUrlView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AnalysisSerializer
    parser =

    def get(self, request, *args, **kwargs):
        """
        Find the privacy policy from the given url. Classify on corpus data to
        analyze the document and parse out the main points in correspondence to the
        actions ("access", "store", "sell", "disclose", "delete").

        :return: Response<JSON>
        """
        params = UrlQueryParamSerizlizer(data=request.GET)
        if not params.is_valid():
            return Response(params.errors, status=HTTP_400_BAD_REQUEST)

        # Locate privacy policy url
        url = params.data.get("url")
        site = session.get(url)
        links = site.html.links
        privacy_policy_url = find_privacy_policy_url(site, html)

        # # Download policy html & parse out text
        # text = text_from_html(driver.pagr_source)

        # For each action, create an action dict --> ActionSerializer
        actions = ("access", "store", "sell", "disclose", "delete")
        return_data = dict(
            actions=[get_fuzzy_result(action, text="") for action in actions],
            privacy_policy_link=privacy_policy_url,
        )
        serializer = self.serializer_class(return_data)
        return Response(serializer.data, status=HTTP_200_OK)
