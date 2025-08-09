import logging

from interface.models import User, Filter


class UserDataProcessor:
    def process_user_data(self, request, **kwargs) -> dict:
        page, model_type, data_to_model, token, user_id = self.get_page_data(request, **kwargs)

        if token and user_id:
            user = User.objects.get(token=token, t_id=int(user_id))
            if user:
                data = model_type(user=user, **data_to_model)
                context = {'data': data}
                try:
                    context['filters_count'] = data.count()
                except AttributeError:
                    pass
                return {'request': request, 'template_name': page, 'context': context}
        return dict()

    def get_page_data(self, request, **kwargs):
        if kwargs.get('filter_id'):
            page = f'interface/current_filter.html'
            data_to_model = {'pk': kwargs.get('filter_id')}
            token, user_id = request.META.get('HTTP_AUTHORIZATION'), request.META.get('HTTP_USER_ID')
            model_type = Filter.objects.get
        else:
            page = f'interface/{kwargs.get("page")}.html'
            data_to_model = {}
            token, user_id = self.get_token_and_id(request)
            model_type = Filter.objects.filter
        return page, model_type, data_to_model, token, user_id

    def get_token_and_id(self, request):
        param_token, param_user = request.GET.get('token'), request.GET.get('user_id')
        header_token, header_user = request.META.get('HTTP_AUTHORIZATION'), request.META.get('HTTP_USER_ID')

        token = param_token if param_token else header_token
        user_id = param_user if param_user else header_user
        return token, user_id

    def is_started(self, request):
        started_param = request.query_params.get('started')
        if started_param and started_param.lower() == 'true':
            return True
        return False
