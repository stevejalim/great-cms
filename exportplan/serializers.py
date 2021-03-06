from rest_framework import serializers


class ExportPlanRecommendedCountriesSerializer(serializers.Serializer):
    sectors = serializers.ListField(child=serializers.CharField())

    def validate_sectors(self, value):
        return value[0].split(',')


class PopulationDataSerializer(serializers.Serializer):
    target_age_groups = serializers.ListField(child=serializers.CharField())
    country = serializers.CharField()

    def validate_target_age_groups(self, value):
        return value[0].split(',')


class AboutYourBuinessSerializer(serializers.Serializer):
    story = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    processes = serializers.CharField(required=False, allow_blank=True)
    packaging = serializers.CharField(required=False, allow_blank=True)
    performance = serializers.CharField(required=False, allow_blank=True)


class ObjectiveSerializer(serializers.Serializer):
    rationale = serializers.CharField(required=False, allow_blank=True)


class TargetMarketsResearchSerializer(serializers.Serializer):
    demand = serializers.CharField(required=False, allow_blank=True)
    competitors = serializers.CharField(required=False, allow_blank=True)
    trend = serializers.CharField(required=False, allow_blank=True)
    unqiue_selling_proposition = serializers.CharField(required=False, allow_blank=True)
    average_price = serializers.IntegerField(required=False, allow_null=True)


class MarketingApproachSerializer(serializers.Serializer):
    resources = serializers.CharField(required=False, allow_blank=True)


class AdaptationTargetMarketSerializer(serializers.Serializer):
    labelling = serializers.CharField(required=False, allow_blank=True)
    packaging = serializers.CharField(required=False, allow_null=True)
    size = serializers.CharField(required=False, allow_null=True)
    standards = serializers.CharField(required=False, allow_null=True)
    translations = serializers.CharField(required=False, allow_null=True)
    other_changes = serializers.CharField(required=False, allow_null=True)
    certificate_of_origin = serializers.CharField(required=False, allow_null=True)
    insurance_certificate = serializers.CharField(required=False, allow_null=True)
    commercial_invoice = serializers.CharField(required=False, allow_null=True)
    uk_customs_declaration = serializers.CharField(required=False, allow_null=True)


class ExportPlanCountrySerializer(serializers.Serializer):
    country_name = serializers.CharField(required=True)
    country_iso2_code = serializers.CharField(required=False, allow_null=True)
    region = serializers.CharField(required=False, allow_null=True)


class ExportPlanCommodityCodeSerializer(serializers.Serializer):
    commodity_name = serializers.CharField(required=True)
    commodity_code = serializers.CharField(required=True)


class ExportPlanSerializer(serializers.Serializer):
    export_commodity_codes = ExportPlanCommodityCodeSerializer(many=True, required=False)
    export_countries = ExportPlanCountrySerializer(many=True, required=False)
    target_markets = serializers.ListField(child=serializers.CharField(), required=False)
    about_your_business = AboutYourBuinessSerializer(required=False)
    objectives = ObjectiveSerializer(required=False)
    target_markets_research = TargetMarketsResearchSerializer(required=False)
    marketing_approach = MarketingApproachSerializer(required=False)
    adaptation_target_market = AdaptationTargetMarketSerializer(required=False)

    def validate_target_markets(self, values):
        return [{'country': c} for c in values]


class CompanyObjectiveSerializer(serializers.Serializer):
    description = serializers.CharField(required=False, allow_blank=True)
    planned_reviews = serializers.CharField(required=False, allow_blank=True)
    owner = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    end_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    companyexportplan = serializers.IntegerField()
    pk = serializers.IntegerField()

    # convert empty strings to null values
    def validate_start_date(self, value):
        if value == '':
            return None
        return value

    def validate_end_date(self, value):
        if value == '':
            return None
        return value


class RouteToMarketSerializer(serializers.Serializer):
    route = serializers.CharField(required=False, allow_blank=True)
    promote = serializers.CharField(required=False, allow_blank=True)
    market_promotional_channel = serializers.CharField(required=False, allow_blank=True)
    companyexportplan = serializers.IntegerField()
    pk = serializers.IntegerField()


class TargetMarketDocumentSerializer(serializers.Serializer):
    document_name = serializers.CharField(required=False, allow_blank=True)
    note = serializers.CharField(required=False, allow_blank=True)
    companyexportplan = serializers.IntegerField()
    pk = serializers.IntegerField()


class NewTargetMarketDocumentSerializer(TargetMarketDocumentSerializer):
    pk = serializers.IntegerField(required=False)


class NewRouteToMarketSerializer(RouteToMarketSerializer):
    pk = serializers.IntegerField(required=False)


class NewObjectiveSerializer(CompanyObjectiveSerializer):
    pk = serializers.IntegerField(required=False)


class PkOnlySerializer(serializers.Serializer):
    pk = serializers.IntegerField()
