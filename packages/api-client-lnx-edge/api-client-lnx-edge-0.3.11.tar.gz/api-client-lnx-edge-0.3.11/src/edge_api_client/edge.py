import os
import requests
from typing import List, Tuple
from datetime import datetime, date

from .base import BaseAPIClient
from .utilities import get_dayparting, format_adjustment_date, build_filters, build_daterange
from .utilities.schemas import CreateOfferSchema, AffiliateOfferSettingsSchema, EditRequestSchema, \
    EditOfferSchema, GetBulkRequestsSchema, EditBulkRequestsSchema


class EdgeAPI(BaseAPIClient):

    def __init__(self, api_key=None, staging=False):
        super(EdgeAPI, self).__init__()

        if staging:
            self.base_url = 'https://edge-staging.com/'
            environ_key = 'EDGE_STAGING_API_KEY'
        else:
            self.base_url = 'https://go-api.leadnomics.com/'
            environ_key = 'EDGE_API_KEY'

        self.staging = staging

        try:
            self.session.headers.update({
                'X-Edge-Key': api_key if api_key else os.environ[environ_key]
            })
        except KeyError:
            raise KeyError('`{}` environment variable not found and no api_key specified.'.format(environ_key))

    @property
    def environment(self):
        return 'staging' if self.staging else 'production'

    def get_offers(self, entity_id=None, **kwargs) -> requests.Response:
        """ Get all offers or specify by `entity_id`

        :param entity_id: (optional) an Edge offer ID. Returns all offers if not specified.
        :return: response
        """
        return self.get_entity('offers', entity_id=entity_id, **kwargs)

    def get_advertisers(self, entity_id=None, **kwargs) -> requests.Response:
        """ Get all advertisers or specify by `entity_id`

        :param entity_id: (optional) an Edge Advertiser ID. Returns all advertisers if not specified.
        :return: response
        """
        return self.get_entity('advertisers', entity_id=entity_id, **kwargs)

    def get_affiliates(self, entity_id=None, **kwargs) -> requests.Response:
        """ Get all affiliates or specify by `entity_id`

        :param entity_id: (optional) an Edge Affiliate ID. Returns all affiliates if not specified.
        :return: response
        """
        return self.get_entity('affiliates', entity_id=entity_id, **kwargs)

    def get_products(self, entity_id=None, **kwargs) -> requests.Response:
        """ Get all products or limit to advertiser with `entity_id`

        :param entity_id: (optional) an Edge Advertiser ID. Returns all products if not specified.
        :return: response
        """
        params = {'advertiser_id': entity_id} if entity_id else {}
        return self.get_entity('products', params=params, **kwargs)

    def get_request(self, request_id, **kwargs) -> requests.Response:
        """ Get metadata for an Edge request.

        :param request_id: an Edge request ID
        :return: response
        """
        return self.get_entity('requests', entity_id=request_id, **kwargs)
    
    def get_bulk_requests(self, body: GetBulkRequestsSchema, **kwargs) -> requests.Response:
        """ Get Edge request objects in bulk.

        :param body: request body. format: {'requestIds': List[str]}
        :return: response
        """
        schema = GetBulkRequestsSchema()
        json_data = schema.load(body)
        return self._post('api/requests/bulk/get', json=schema.dump(json_data), **kwargs)
    
    def edit_bulk_requests(self, body: EditBulkRequestsSchema, **kwargs) -> requests.Response:
        """ Edit the isTest status of many Edge requests at once.

        :param body: request body. format: {'requestIds': List[str], 'isTest': boolean}
        :return: response
        """
        schema = EditBulkRequestsSchema()
        json_data = schema.dump(schema.load(body))
        json_data['isTest'] = 1 if bool(json_data['isTest']) else 0
        return self._patch('api/requests/bulk/edit', json=json_data, **kwargs)

    def edit_request(self, request_id: str, request_edit_body: dict) -> requests.Response:
        """ Edit an existing Edge request.

        :param request_id: Edge request ID
        :param request_edit_body: a valid PATCH body
        :return: response
        """
        schema = EditRequestSchema()
        json_data = schema.load(request_edit_body)
        return self.patch_entity('requests', entity_id=request_id, patch_json=schema.dump(json_data))

    def get_past_changes(self, **kwargs) -> requests.Response:
        """ Return executed changes recorded in Changelog. """
        return self.get_entity('api/audit/search/', **kwargs)

    def get_scheduled_changes(self, **kwargs) -> requests.Response:
        """ Return scheduled changes that have yet to be executed. """
        return self._post('api/schedule/search', **kwargs)

    def get_affiliate_offer_settings(self, affiliate_id, offer_id, **kwargs) -> requests.Response:
        """ Return affiliate offer settings for a given aff+offer.

        :param affiliate_id: valid affiliate ID
        :param offer_id: valid offer ID
        :return: response
        """
        params = {'affiliateId': str(affiliate_id), 'offerId': str(offer_id)}
        return self.get_entity('affiliate-offer-settings', params=params, **kwargs)

    def create_offer(self,
                     friendly_name: str = None,
                     category: int = None,
                     description: str = None,
                     domain: int = None,
                     error_fallback_url: str = None,
                     filter_fallback_url: str = None,
                     filter_fallback_product: str = None,
                     dayparting: dict = None,
                     filters: List[dict] = None,
                     destination: dict = None,
                     status: str = 'Active',
                     viewability: str = 'Testing',  # default
                     scrub: int = None,
                     default_affiliate_conversion_cap: int = None,
                     lifetime_affiliate_click_cap: int = None,
                     traffic_types: List = None,
                     pixel_behavior: str = 'dedupe',
                     allow_query_passthrough: bool = False,
                     allow_pageview_pixel: bool = False,
                     allow_forced_click_conversion: bool = False,
                     creatives: List[int] = None,
                     traffic_type: str = None,
                     unsubscribe_link: str = None,
                     suppression_list: str = None,
                     from_lines: str = None,
                     subject_lines: str = None,
                     redirect_offer: int = None,
                     redirect_percent: float = None,
                     cap_redirect_offer: int = None,
                     **kwargs
                     ) -> requests.Response:
        """ Create an offer object. Must be an admin.

        :param friendly_name: offer name
        :param category: vertical ID from goodmeasure
        :param description: offer description text (markdown optional, detected on front-end)
        :param domain: offer default domain ID from goodmeasure
        :param error_fallback_url: offer error url
        :param filter_fallback_url: offer fallback url
        :param filter_fallback_product: offer filter fallback product ID from goodmeasure
        :param dayparting: a dayparting schedule   # TODO: Document this
        :param filters: a list of dictionaries defining Edge offer filters
        :param destination: offer destination fields
        :param status: offer status, defaults to Active
        :param viewability: offer viewability, defaults to Testing
        :param scrub: offer offset, defaults to 0
        :param default_affiliate_conversion_cap: defaults to 0
        :param lifetime_affiliate_click_cap: defaults to 0
        :param traffic_types: list of valid traffic types, defaults to All  # TODO: document
        :param pixel_behavior: offer pixel behavior, defaults to dedupe
        :param allow_query_passthrough: boolean, defaults to False
        :param allow_pageview_pixel: boolean, defaults to False
        :param allow_forced_click_conversion: boolean, defaults to False
        :param creatives: creative objects....ignore this and upload manually for right now IMO  # TODO
        :param unsubscribe_link: optional
        :param suppression_list: optional
        :param from_lines: optional
        :param subject_lines: optional
        :param redirect_offer: defaults to none
        :param redirect_percent: defaults to 0
        :param cap_redirect_offer: defaults to none
        :return: response
        """

        if not filters:
            filters = {'filters': []}

        body = {
            'friendlyName': friendly_name or kwargs.get('friendlyName'),
            'category': category,
            'domain': domain,
            'customFallbackUrl': error_fallback_url or kwargs.get('customFallbackUrl'),
            'filterFallbackUrl': filter_fallback_url or kwargs.get('filterFallbackUrl'),
            'filterFallbackProduct': filter_fallback_product or kwargs.get('filterFallbackProduct'),
            'dayparting': {},
            'filters': filters,
            'destination': destination,
            'status': status,
            'viewability': viewability,
            'scrub': scrub,
            'defaultAffiliateConvCap': default_affiliate_conversion_cap or kwargs.get('defaultAffiliateConvCap'),
            'lifetimeAffiliateClickCap': lifetime_affiliate_click_cap or kwargs.get('lifetimeAffiliateClickCap'),
            'trafficTypes': traffic_types or kwargs.get('trafficTypes') or [],
            'pixelBehavior': pixel_behavior or kwargs.get('pixelBehavior'),
            'allowQueryPassthrough': allow_query_passthrough or kwargs.get('allowQueryPassthrough'),
            'allowPageviewPixel': allow_pageview_pixel or kwargs.get('allowPageviewPixel'),
            'allowForcedClickConversion': allow_forced_click_conversion or kwargs.get('allowForcedClickConversion'),
            'trafficType': traffic_type or kwargs.get('trafficType', 'Click'),
            'unsubscribe_link': unsubscribe_link,
            'suppression_list': suppression_list,
            'from_lines': from_lines,
            'subject_lines': subject_lines,
            'redirectOffer': redirect_offer or kwargs.get('redirectOffer'),
            'redirectPercent': redirect_percent or kwargs.get('redirectPercent'),
            'capRedirectOffer': cap_redirect_offer or kwargs.get('capRedirectOffer')
        }

        if description:
            body['description'] = description

        if dayparting:
            if not any([x.get('type') == 'weekHour' for x in body['filters']['filters']]):
                body['filters']['filters'].append({
                    'type': 'weekHour',
                    'include': get_dayparting(dayparting)
                })
            else:
                raise ValueError('Providing both `dayparting` and a `weekHour` filter is ambiguous.')

        schema = CreateOfferSchema()
        json_data = schema.load({k: v for k, v in body.items() if v is not None})

        return self._post('api/offers', json=schema.dump(json_data))
    
    def edit_offer(self, offer_id: int, offer_body: EditOfferSchema) -> requests.Response:
        """ Edit/update an offer object. """
        schema = EditOfferSchema()
        json_data = schema.load(offer_body)
        return self._put('api/offers/{}'.format(offer_id), json=schema.dump(json_data))

    def _get_report(self,
                    dimensions: list,
                    start_date: Tuple[datetime, date, str],
                    end_date: Tuple[datetime, date, str],
                    timezone: str = 'America/New_York',
                    metrics: list = None,
                    filters: list = None,
                    rows_per_page: int = 10000,
                    row_offset: int = 0,
                    **kwargs) -> requests.Response:
        """ Get a report with arguments. """
        report_config = {
            'dimensions': dimensions,
            'metrics': metrics or ['sessions', 'clicks', 'conversions', 'paidConversions', 'lnxRevenue', 'lnxCost'],
            'dateRange': build_daterange(start_date, end_date),
            'timezone': timezone,
            'filters': build_filters(filters or [], **kwargs),
            'tableSort': {},
            'rowsPerPage': rows_per_page,
            'rowOffset': row_offset
        }

        # Overrides report_config with passed-in kwargs, but doesn't add any NEW keys to dict. Allows user to pass
        #  filters like `affiliate_id=XXXX` with ease.
        report_config.update((k, kwargs[k]) for k in report_config.keys() & kwargs.keys())

        resp = self._post('api/reports', json=report_config)

        return resp

    def get_advertiser_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default advertiser report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['advertiserId', 'advertiserName'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_affiliate_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default affiliate report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['affiliateId', 'affiliateCompany'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_click_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default click report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['clickId', 'created_on', 'affiliateId', 'affiliateCompany', 'offerId', 'offerName',
                        's1', 's2', 's3', 's4', 's5', 'ipaddress', 'go_disposition'],
            metrics=['conversions', 'paidConversions', 'lnxProfit', 'lnxRevenue', 'lnxCost'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_daily_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default daily report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['timestampDay'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_hourly_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default hourly report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['timestampDay', 'hourOfDay'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_offer_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default offer report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['offerId', 'offerName'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_paid_conversion_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default paid conversion report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['clickId', 'created_on', 'affiliateId', 'affiliateCompany', 'offerId', 'offerName',
                        's1', 's2', 's3', 's4', 's5', 'ipaddress'],
            metrics=['lnxProfit', 'lnxRevenue', 'lnxCost'],
            filters=[{'type': 'gt', 'value': 0, 'column': 'paidConversions'}],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_product_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default product report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['productId', 'productName'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_sessions_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default sessions report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['clickId', 'created_on', 'affiliateId', 'affiliateCompany', 'offerId', 'offerName',
                        's1', 's2', 's3', 's4', 's5', 'ipaddress', 'go_disposition'],
            metrics=['clicks', 'conversions', 'paidConversions', 'lnxProfit', 'lnxRevenue', 'lnxCost'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_suboffer_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default suboffer report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['subOfferId', 'subOfferName'],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_total_conversion_report(self, start_date: Tuple[datetime, date, str], end_date: Tuple[datetime, date, str], **kwargs) -> requests.Response:
        """ Get default total conversion report.

        :param start_date: YYYY-MM-DD date
        :param end_date: YYYY-MM-DD date
        :return: response
        """
        return self._get_report(
            dimensions=['clickId', 'created_on', 'affiliateId', 'affiliateCompany', 'offerId', 'offerName',
                        's1', 's2', 's3', 's4', 's5', 'ipaddress'],
            metrics=['lnxProfit', 'lnxRevenue', 'lnxCost'],
            filters=[{'type': 'gt', 'value': 0, 'column': 'conversions'}],
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

    def get_custom_report(self, report_config, **kwargs) -> requests.Response:
        """ Get a custom report with a json body.

        :param report_config: a valid Edge report config body
        :return: response
        """
        return self._post('api/reports', json=report_config, **kwargs)

    def adjust(self, affiliate_id, offer_id_path: list, created_on: str, click_adjustment=0, conversion_adjustment=0,
               total_conversion_adjustment=0, conversion_amount_adjustment=0.00, payout_adjustment=0.00) -> requests.Response:
        data = {
            'affiliateId': affiliate_id,
            'offerIdPath': offer_id_path,
            'clickAdjustment': click_adjustment,
            'conversionAdjustment': conversion_adjustment,  # Paid conv, and total if that's not provided
            'conversionAmountAdjustment': conversion_amount_adjustment,
            'payoutAdjustment': payout_adjustment,
            'createdOn': format_adjustment_date(created_on)
        }

        if total_conversion_adjustment:
            data['totalConversionAdjustment'] = total_conversion_adjustment

        resp = self._post('api/adjust-stats', json=data)

        return resp

        # TODO: get ALL entities. Including verticals, domains, etc.

    def get_offer_approvals(self, offer_id, **kwargs) -> requests.Response:
        """ Given an offer ID, return all approved affiliates.

        :param offer_id: an Edge offer ID
        :return: response object
        """
        return self._get('api/offers/{}/affiliates'.format(offer_id), **kwargs)
    
    def update_affiliate_offer_settings(self, settings: List[dict], **kwargs) -> requests.Response:
        """ Change an affiliate's aff+offer settings. Please see API docs for route PUT `/api/affiliate-offer-settings` 
        for a valid schema definition.

        :param settings: new affiliate offer settings represented as JSON (a list of dicts)
        :type settings: List[dict]
        :return: response object
        """
        if not settings:
            settings = [{}]

        aos_schema = AffiliateOfferSettingsSchema(many=True)
        json_data = aos_schema.load(settings)

        return self._put('api/affiliate-offer-settings', json=aos_schema.dump(json_data), **kwargs)
    
    def change_affiliate_offer_approval(self, affiliate_id, offer_id, status: str, **kwargs) -> requests.Response:
        """ Change the application status on a specific offer for an affiliate. Please see API docs for 
        route PUT `/api/affiliate-offer-settings` for a valid schema definition.

        :param affiliate_id: an Edge affiliate ID
        :param offer_id: an Edge offer ID
        :param status: a valid application status. One of: Applied, Denied, Approved
        :return: response object
        """
        body = [{
            'affiliateId': affiliate_id,
            'offerId': offer_id,
            'status': status
        }]

        return self.update_affiliate_offer_settings(settings=body, **kwargs)
    
    def get_saved_reports(self, uuid: str = None, **kwargs) -> requests.Response:
        """ Get all affiliates or specify by `uuid`

        :param uuid: (optional) an Edge saved report ID. Returns all saved reports if not specified.
        :type uuid: str, optional
        :return: response object
        """
        return self.get_entity('saved-reports', entity_id=uuid, **kwargs)

    def create_saved_report(self, name: str, report_config: dict, **kwargs) -> requests.Response:
        """ Create a saved report.

        :param name: report name
        :param report_config: valid Edge report config body
        :type report_config: dict
        :return: response object
        """
        body = {
            'name': name,
            'report': report_config
        }

        return self._post('api/saved-reports', json=body, **kwargs)
    
    def patch_saved_report(self, uuid: str, name: str = None, report_config: dict = None, **kwargs) -> requests.Response:
        """ Update or rename a saved report. Must provide either `name` or `report_config`

        :param uuid: existing saved report UUID
        :param name: new name for the saved report. may omit to only alter the report config body.
        :type name: str, optional
        :param report_config: new report_config body. may omit when simply renaming saved reports
        :type report_config: dict, optional
        :raises ValueError: error raised when user fails to provide a `name` or `report_config`.
        :return: response object
        """
        if not name and not report_config:
            raise ValueError('Must provide `name`, `report_config`, or both.')
        body = {}
        if name: 
            body['name'] = name
        if report_config:
            body['report_config'] = report_config

        return self._patch('api/saved-reports/{}'.format(uuid), json=body, **kwargs)

    def delete_saved_report(self, uuid: str, **kwargs) -> requests.Response:
        """ Delete a saved report.

        :param uuid: saved report UUID
        :return: response object
        """
        return self._delete('api/saved-reports/{}'.format(uuid), **kwargs)

    def __repr__(self):
        return f'EdgeAPI(staging={self.staging})'
