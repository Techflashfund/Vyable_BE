# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Databasechangelog(models.Model):
    id = models.CharField(primary_key=True,max_length=255)
    author = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    dateexecuted = models.DateTimeField()
    orderexecuted = models.IntegerField()
    exectype = models.CharField(max_length=10)
    md5sum = models.CharField(max_length=35, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    liquibase = models.CharField(max_length=20, blank=True, null=True)
    contexts = models.CharField(max_length=255, blank=True, null=True)
    labels = models.CharField(max_length=255, blank=True, null=True)
    deployment_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'databasechangelog'


class Databasechangeloglock(models.Model):
    id = models.IntegerField(primary_key=True)
    locked = models.BooleanField()
    lockgranted = models.DateTimeField(blank=True, null=True)
    lockedby = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'databasechangeloglock'


class TblAmcDetails(models.Model):
    amc_code = models.CharField(primary_key=True, max_length=255)
    amc_name = models.CharField(max_length=258)
    amc_document_url = models.CharField(max_length=1000)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_amc_details'


class TblNavHistoryMaster(models.Model):
    pk = models.CompositePrimaryKey('isin', 'nav_date')
    isin = models.CharField(max_length=12)
    nav_date = models.DateTimeField()
    nav_value = models.DecimalField(max_digits=20, decimal_places=4)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_nav_history_master'
        unique_together = (('isin', 'nav_date'),)


class TblNavMaster(models.Model):
    nav_date = models.DateField()
    scheme_code = models.CharField(max_length=20)
    scheme_name = models.CharField(max_length=250)
    rta_scheme_code = models.CharField(max_length=6)
    div_reinvest_flag = models.CharField(max_length=5)
    isin = models.CharField(primary_key=True, max_length=12)
    nav_value = models.DecimalField(max_digits=20, decimal_places=4)
    rta_code = models.CharField(max_length=20)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_nav_master'


class TblSchemeDetails(models.Model):
    isin = models.CharField(primary_key=True, max_length=12)
    fund_type = models.CharField(blank=True, null=True)
    riskometer_launch = models.CharField(blank=True, null=True)
    riskometer = models.CharField(blank=True, null=True)
    category = models.CharField(blank=True, null=True)
    objective = models.CharField(blank=True, null=True)
    fund_manager = models.CharField(blank=True, null=True)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_scheme_details'


class TblSchemeMaster(models.Model):
    unique_no = models.CharField(primary_key=True, max_length=5)
    scheme_code = models.CharField(max_length=20)
    rta_scheme_code = models.CharField(max_length=6)
    amc_scheme_code = models.CharField(max_length=10)
    amc_code = models.CharField(max_length=255)
    isin = models.CharField(max_length=12)
    scheme_type = models.CharField(max_length=20)
    scheme_plan = models.CharField(max_length=10, blank=True, null=True)
    scheme_name = models.CharField(max_length=250, blank=True, null=True)
    purchase_allowed = models.CharField(max_length=1, blank=True, null=True)
    purchase_transaction_mode = models.CharField(max_length=2, blank=True, null=True)
    minimum_purchase_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    additional_purchase_amount_multiple = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    maximum_purchase_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    purchase_amount_multiplier = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    purchase_cutoff_time = models.TimeField(blank=True, null=True)
    redemption_allowed = models.CharField(max_length=1, blank=True, null=True)
    redemption_transaction_mode = models.CharField(max_length=50, blank=True, null=True)
    minimum_redemption_qty = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    redemption_qty_multiplier = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    maximum_redemption_qty = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    redemption_amount_minimum = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    redemption_amount_maximum = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    redemption_amount_multiple = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    redemption_cut_off_time = models.TimeField(blank=True, null=True)
    rta_agent_code = models.CharField(max_length=50, blank=True, null=True)
    amc_active_flag = models.BigIntegerField(blank=True, null=True)
    divident_reinvestment_flag = models.CharField(max_length=1, blank=True, null=True)
    sip_flag = models.CharField(max_length=1, blank=True, null=True)
    stp_flag = models.CharField(max_length=1, blank=True, null=True)
    swp_flag = models.CharField(max_length=1, blank=True, null=True)
    switch_flag = models.CharField(max_length=1, blank=True, null=True)
    settlement_type = models.CharField(max_length=3, blank=True, null=True)
    amc_ind = models.CharField(max_length=3, blank=True, null=True)
    face_value = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    exit_load_flag = models.CharField(max_length=1, blank=True, null=True)
    exit_load = models.CharField(max_length=600, blank=True, null=True)
    lock_in_period_flag = models.CharField(max_length=1, blank=True, null=True)
    lock_in_period = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    channel_partner_code = models.CharField(max_length=20, blank=True, null=True)
    reopening_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_scheme_master'


class TblSchemePortfolio(models.Model):
    id = models.BigIntegerField(primary_key=True)
    isin = models.CharField()
    denomination = models.CharField()
    instrument_name = models.CharField()
    sector = models.CharField(blank=True, null=True)
    asset_class = models.CharField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    allocation = models.FloatField()
    investment = models.FloatField()
    rating = models.CharField(blank=True, null=True)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_scheme_portfolio'


class TblSipSchemeMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    amc_code = models.CharField(max_length=250)
    amc_name = models.CharField(max_length=50)
    scheme_code = models.CharField(max_length=50)
    scheme_name = models.CharField(max_length=1000)
    sip_transaction_mode = models.CharField(max_length=50)
    sip_frequency = models.CharField(max_length=50)
    sip_dates = models.CharField(max_length=1000)
    sip_minimum_gap = models.BigIntegerField()
    sip_maximum_gap = models.BigIntegerField()
    sip_installment_gap = models.BigIntegerField()
    sip_minimum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    sip_maximum_installment_amount = models.CharField(max_length=50)
    sip_multiplier_amount = models.DecimalField(max_digits=100, decimal_places=4)
    sip_minimum_installment_numbers = models.BigIntegerField()
    sip_maximum_installment_numbers = models.BigIntegerField()
    scheme_isin = models.CharField(max_length=50)
    scheme_type = models.CharField(max_length=50)
    pause_minimum_installments = models.BigIntegerField(blank=True, null=True)
    pause_maximum_installments = models.BigIntegerField(blank=True, null=True)
    pause_modification_count = models.BigIntegerField(blank=True, null=True)
    filler1 = models.CharField(max_length=255, blank=True, null=True)
    filler2 = models.CharField(max_length=255, blank=True, null=True)
    filler3 = models.CharField(max_length=255, blank=True, null=True)
    filler4 = models.CharField(max_length=255, blank=True, null=True)
    filler5 = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    pause_flag = models.BooleanField(blank=True, null=True)
    sip_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_sip_scheme_master'


class TblStpSchemeMaster(models.Model):
    id = models.BigIntegerField(primary_key=True)
    amc_code = models.CharField(max_length=250)
    bse_scheme_code = models.CharField(max_length=50)
    scheme_name = models.CharField(max_length=1000)
    scheme_isin = models.CharField(max_length=50)
    scheme_type = models.CharField(max_length=50)
    astp_transaction_mode = models.CharField(max_length=50)
    astp_in_minimum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_in_maximum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_in_multiplier_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_out_minimum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_out_maximum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_frequency = models.CharField(max_length=50)
    astp_out_multiplier_amount = models.DecimalField(max_digits=100, decimal_places=4)
    astp_minimum_installment_units = models.DecimalField(max_digits=100, decimal_places=4)
    astp_maximum_installment_units = models.DecimalField(max_digits=100, decimal_places=4)
    astp_multiplier_units = models.DecimalField(max_digits=100, decimal_places=4)
    astp_minimum_installment_numbers = models.BigIntegerField()
    astp_maximum_installment_numbers = models.BigIntegerField()
    astp_reg_in = models.CharField(max_length=50)
    astp_reg_out = models.CharField(max_length=50)
    astp_dates = models.CharField(max_length=1000, blank=True, null=True)
    astp_minimum_gap = models.BigIntegerField()
    astp_maximum_gap = models.BigIntegerField()
    astp_installment_gap = models.BigIntegerField()
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    astp_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_stp_scheme_master'


class TblSwpSchemeMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    amc_code = models.CharField(max_length=250)
    amc_name = models.CharField(max_length=1000)
    bse_scheme_code = models.CharField(max_length=50)
    scheme_name = models.CharField(max_length=1000)
    scheme_isin = models.CharField(max_length=50)
    scheme_type = models.CharField(max_length=50)
    aswp_transaction_mode = models.CharField(max_length=50)
    aswp_minimum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_maximum_installment_amount = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_multiplier_amount = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_minimum_installment_units = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_maximum_installment_units = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_multiplier_units = models.DecimalField(max_digits=100, decimal_places=4)
    aswp_minimum_installment_numbers = models.BigIntegerField()
    aswp_maximum_installment_numbers = models.BigIntegerField()
    aswp_frequency = models.CharField(max_length=50)
    aswp_dates = models.CharField(max_length=1000)
    aswp_minimum_gap = models.BigIntegerField()
    aswp_maximum_gap = models.BigIntegerField()
    aswp_installment_gap = models.BigIntegerField()
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    aswp_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_swp_scheme_master'

