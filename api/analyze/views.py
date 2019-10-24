# [Django]
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

# [App]
from api.analyze.serializers import UrlQueryParamSerizlizer, AnalysisSerializer
from api.analyze.utils import (
    find_privacy_policy_url,
    download_html,
    text_from_html,
    get_fuzzy_result,
)


class AnalyzeUrlView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AnalysisSerializer

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
        privacy_policy_url = find_privacy_policy_url(params.data.get("url"))

        # Download policy html & parse out text
        html = download_html(privacy_policy_url)
        text = text_from_html(body=html)

        # For each action, create an action dict --> ActionSerializer
        actions = ("access", "store", "sell", "disclose", "delete")
        return_data = dict(
            actions=[get_fuzzy_result(action, text=text) for action in actions],
            privacy_policy_link=privacy_policy_url,
        )
        serializer = self.serializer_class(return_data)
        return Response(serializer.data, status=HTTP_200_OK)
