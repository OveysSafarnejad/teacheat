from rest_framework.filters import OrderingFilter


class CoreOrderingFilter(OrderingFilter):
    fields = dict()

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = list()
            for param in params.split(','):
                param = param.strip()
                if param[0] == '-':
                    param = param.strip('-')
                    field = self.fields.get(param, param)
                    field = '-' + field
                else:
                    field = self.fields.get(param, param)

                fields.append(field)

            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)
