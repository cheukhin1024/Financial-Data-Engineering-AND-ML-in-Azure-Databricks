# Databricks notebook source
#Example: https://databricks.com/notebooks/segment-p13n//sg_03_clustering.html

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.model_selection import train_test_split
from sklearn import metrics

import os

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors

import numpy as np
import pyspark.pandas as ps

#import mlflow.sklearn

# COMMAND ----------

spark.sql("set spark.databricks.delta.autoCompact.enabled = true")

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC Use deltabase

# COMMAND ----------


data_test = spark.sql("SELECT AAPL_dateTime, \
                              AA_adjClose \
                       FROM deltabase.aapl_30min_delta \
                       FULL JOIN deltabase.aa_30min_delta ON aapl_30min_delta.AAPL_dateTime = AA_dateTime")

# COMMAND ----------

data = spark.sql("SELECT AAPL_adjClose, \
                         AA_adjClose, \
                         AAL_adjClose, \
                         AAP_adjClose, \
                         A_adjClose, \
                         ABBV_adjClose, \
                         ABC_adjClose, \
                         ABMD_adjClose, \
                         ABT_adjClose, \
                         ACN_adjClose, \
                         ACV_adjClose, \
                         ADBE_adjClose, \
                         ADI_adjClose, \
                         ADM_adjClose, \
                         ADP_adjClose, \
                         ADS_adjClose, \
                         ADSK_adjClose, \
                         ADT_adjClose, \
                         AEE_adjClose, \
                         AEP_adjClose, \
                         AES_adjClose, \
                         AFL_adjClose, \
                         AIG_adjClose, \
                         AINV_adjClose, \
                         AIV_adjClose, \
                         AIZ_adjClose, \
                         AJG_adjClose, \
                         AKAM_adjClose, \
                         ALB_adjClose, \
                         ALGN_adjClose, \
                         ALK_adjClose, \
                         ALL_adjClose, \
                         ALLE_adjClose, \
                         ALTR_adjClose, \
                         AMAT_adjClose, \
                         AMBC_adjClose, \
                         AMCR_adjClose, \
                         AMD_adjClose, \
                         AME_adjClose, \
                         AMG_adjClose, \
                         AMGN_adjClose, \
                         AMP_adjClose, \
                         AMT_adjClose, \
                         AMZN_adjClose \
                         AN_adjClose, \
                         ANET_adjClose, \
                         ANF_adjClose, \
                         ANSS_adjClose, \
                         ANTM_adjClose, \
                         AON_adjClose, \
                         AOS_adjClose, \
                         APA_adjClose, \
                         APD_adjClose, \
                         APH_adjClose, \
                         APTV_adjClose, \
                         ARE_adjClose, \
                         ARNC_adjClose, \
                         ASH_adjClose, \
                         ASO_adjClose, \
                         ATGE_adjClose, \
                         ATI_adjClose, \
                         ATO_adjClose, \
                         ATVI_adjClose, \
                         AVB_adjClose, \
                         AVGO_adjClose, \
                         AVY_adjClose, \
                         AWK_adjClose, \
                         AXP_adjClose, \
                         AYI_adjClose, \
                         AZO_adjClose, \
                         BA_adjClose, \
                         BAC_adjClose, \
                         BAX_adjClose, \
                         BBBY_adjClose, \
                         BBY_adjClose, \
                         BC_adjClose, \
                         BDX_adjClose, \
                         BEN_adjClose, \
                         BFB_adjClose, \
                         BIDU_adjClose, \
                         BIG_adjClose, \
                         BIIB_adjClose, \
                         BIO_adjClose, \
                         BK_adjClose, \
                         BKNG_adjClose, \
                         BLK_adjClose, \
                         BLL_adjClose, \
                         BMRN_adjClose, \
                         BMY_adjClose, \
                         BR_adjClose, \
                         BRKB_adjClose, \
                         BRO_adjClose, \
                         BSX_adjClose, \
                         BTU_adjClose, \
                         BUD_adjClose, \
                         BWA_adjClose, \
                         BXP_adjClose, \
                         C_adjClose, \
                         CAG_adjClose, \
                         CAH_adjClose, \
                         CAR_adjClose, \
                         CARR_adjClose, \
                         CAT_adjClose, \
                         CB_adjClose, \
                         CBH_adjClose, \
                         CBOE_adjClose, \
                         CBRE_adjClose, \
                         CC_adjClose, \
                         CCI_adjClose, \
                         CCK_adjClose, \
                         CCL_adjClose, \
                         CCU_adjClose, \
                         CDAY_adjClose, \
                         CDNS_adjClose, \
                         CDW_adjClose, \
                         CE_adjClose, \
                         CERN_adjClose, \
                         CF_adjClose, \
                         CFG_adjClose, \
                         CHD_adjClose, \
                         CHIR_adjClose, \
                         CHK_adjClose, \
                         CHKP_adjClose, \
                         CHRW_adjClose, \
                         CHTR_adjClose, \
                         CI_adjClose, \
                         CIEN_adjClose, \
                         CINF_adjClose, \
                         CIT_adjClose, \
                         CL_adjClose, \
                         CLF_adjClose, \
                         CLX_adjClose, \
                         CMA_adjClose, \
                         CMCSA_adjClose, \
                         CME_adjClose, \
                         CMG_adjClose, \
                         CMI_adjClose, \
                         CMS_adjClose, \
                         CNC_adjClose, \
                         CNP_adjClose, \
                         CNX_adjClose, \
                         COF_adjClose, \
                         COO_adjClose, \
                         COOP_adjClose, \
                         COP_adjClose, \
                         COST_adjClose, \
                         COTY_adjClose, \
                         CPB_adjClose, \
                         CPRI_adjClose, \
                         CPRT_adjClose, \
                         CPT_adjClose, \
                         CRM_adjClose, \
                         CSCO_adjClose, \
                         CSX_adjClose, \
                         CTAS_adjClose, \
                         CTLT_adjClose, \
                         CTSH_adjClose, \
                         CTVA_adjClose, \
                         CTXS_adjClose, \
                         CVS_adjClose, \
                         CVX_adjClose, \
                         CZR_adjClose, \
                         D_adjClose, \
                         DAL_adjClose, \
                         DAN_adjClose, \
                         DD_adjClose, \
                         DDS_adjClose, \
                         DE_adjClose, \
                         DELL_adjClose, \
                         DFS_adjClose, \
                         DG_adjClose, \
                         DGX_adjClose, \
                         DHI_adjClose, \
                         DHR_adjClose, \
                         DIS_adjClose, \
                         DISCA_adjClose, \
                         DISCK_adjClose, \
                         DISH_adjClose, \
                         DLR_adjClose, \
                         DLTR_adjClose, \
                         DLX_adjClose, \
                         DNB_adjClose, \
                         DOV_adjClose, \
                         DOW_adjClose, \
                         DPZ_adjClose, \
                         DRE_adjClose, \
                         DRI_adjClose, \
                         DTE_adjClose, \
                         DUK_adjClose, \
                         DVA_adjClose, \
                         DVN_adjClose, \
                         DXC_adjClose, \
                         DXCM_adjClose, \
                         EA_adjClose, \
                         EBAY_adjClose, \
                         ECL_adjClose, \
                         ED_adjClose, \
                         EFX_adjClose, \
                         EIX_adjClose, \
                         EL_adjClose, \
                         EMN_adjClose, \
                         EMR_adjClose, \
                         ENDP_adjClose, \
                         ENPH_adjClose, \
                         EOG_adjClose, \
                         EPAM_adjClose, \
                         EQ_adjClose, \
                         EQIX_adjClose, \
                         EQR_adjClose, \
                         EQT_adjClose, \
                         ES_adjClose, \
                         ESS_adjClose, \
                         ETN_adjClose, \
                         ETR_adjClose, \
                         ETSY_adjClose, \
                         EVRG_adjClose, \
                         EW_adjClose, \
                         EXC_adjClose, \
                         EXPD_adjClose, \
                         EXPE_adjClose, \
                         EXR_adjClose, \
                         F_adjClose, \
                         FANG_adjClose, \
                         FAST_adjClose, \
                         FB_adjClose, \
                         FBHS_adjClose, \
                         FCX_adjClose, \
                         FDS_adjClose, \
                         FDX_adjClose, \
                         FE_adjClose, \
                         FFIV_adjClose, \
                         FFHN_adjClose, \
                         FIS_adjClose, \
                         FISV_adjClose, \
                         FITB_adjClose, \
                         FL_adjClose, \
                         FLEX_adjClose \
                         FLR_adjClose, \
                         FLS_adjClose, \
                         FLT_adjClose, \
                         FMC_adjClose, \
                         FOSL_adjClose, \
                         FOX_adjClose, \
                         FOXA_adjClose, \
                         FPL_adjClose, \
                         FRC_adjClose, \
                         FRT_adjClose, \
                         FSLR_adjClose, \
                         FTI_adjClose, \
                         FTNT_adjClose, \
                         FTV_adjClose, \
                         GCI_adjClose, \
                         GD_adjClose, \
                         GE_adjClose, \
                         GHC_adjClose, \
                         GILD_adjClose, \
                         GIS_adjClose, \
                         GL_adjClose, \
                         GLW_adjClose, \
                         GM_adjClose, \
                         GME_adjClose, \
                         GNRC_adjClose, \
                         GNW_adjClose, \
                         GOOG_adjClose, \
                         GOOGL_adjClose, \
                         GP_adjClose, \
                         GPC_adjClose, \
                         GPN_adjClose, \
                         GPS_adjClose, \
                         GRMN_adjClose, \
                         GS_adjClose, \
                         GT_adjClose, \
                         GWW_adjClose, \
                         HAL_adjClose, \
                         HAS_adjClose, \
                         HBAN_adjClose, \
                         HBI_adjClose, \
                         HCA_adjClose, \
                         HD_adjClose, \
                         HES_adjClose, \
                         HFC_adjClose, \
                         HIG_adjClose, \
                         HII_adjClose, \
                         HLT_adjClose, \
                         HOG_adjClose, \
                         HOLX_adjClose, \
                         HON_adjClose, \
                         HP_adjClose, \
                         HPE_adjClose, \
                         HPQ_adjClose, \
                         HRB_adjClose, \
                         HRL_adjClose, \
                         HSIC_adjClose, \
                         HST_adjClose, \
                         HSY_adjClose, \
                         HUM_adjClose, \
                         IAC_adjClose, \
                         IBM_adjClose, \
                         ICE_adjClose, \
                         IDXX_adjClose, \
                         IEX_adjClose, \
                         IFF_adjClose, \
                         IGT_adjClose, \
                         IHRT_adjClose, \
                         ILMN_adjClose, \
                         INCY_adjClose, \
                         INFO_adjClose \
                         INFY_adjClose, \
                         INTC_adjClose, \
                         INTU_adjClose, \
                         IP_adjClose, \
                         IPG_adjClose, \
                         IPGP_adjClose, \
                         IQV_adjClose, \
                         IR_adjClose, \
                         IRM_adjClose, \
                         ISRG_adjClose, \
                         IT_adjClose, \
                         ITT_adjClose, \
                         ITW_adjClose, \
                         IVZ_adjClose, \
                         J_adjClose, \
                         JBHT_adjClose, \
                         JBL_adjClose, \
                         JCI_adjClose, \
                         JD_adjClose, \
                         JEF_adjClose, \
                         JKHY_adjClose, \
                         JNJ_adjClose, \
                         JNPR_adjClose, \
                         JP_adjClose, \
                         JPM_adjClose, \
                         JWN_adjClose, \
                         K_adjClose, \
                         KBH_adjClose, \
                         KEY_adjClose, \
                         KEYS_adjClose, \
                         KHC_adjClose, \
                         KIM_adjClose, \
                         KLAC_adjClose, \
                         KMB_adjClose, \
                         KMI_adjClose, \
                         KMX_adjClose, \
                         KO_adjClose, \
                         KODK_adjClose, \
                         KR_adjClose, \
                         KSS_adjClose, \
                         KSU_adjClose, \
                         L_adjClose, \
                         LBTYK_adjClose, \
                         LDOS_adjClose, \
                         LEG_adjClose, \
                         LEN_adjClose, \
                         LH_adjClose, \
                         LHX_adjClose, \
                         LIFE_adjClose, \
                         LIN_adjClose, \
                         LKQ_adjClose, \
                         LLY_adjClose, \
                         LMT_adjClose, \
                         LNC_adjClose, \
                         LNT_adjClose, \
                         LOGI_adjClose, \
                         LOW_adjClose, \
                         LRCX_adjClose, \
                         LSI_adjClose, \
                         LU_adjClose, \
                         LUMN_adjClose, \
                         LUV_adjClose, \
                         LVS_adjClose, \
                         LW_adjClose, \
                         LYB_adjClose, \
                         LYV_adjClose, \
                         M_adjClose, \
                         MA_adjClose, \
                         MAA_adjClose, \
                         MAC_adjClose, \
                         MAR_adjClose, \
                         MAS_adjClose, \
                         MAT_adjClose, \
                         MBI_adjClose, \
                         MCD_adjClose, \
                         MCHP_adjClose, \
                         MCK_adjClose, \
                         MCO_adjClose, \
                         MDLZ_adjClose, \
                         MDP_adjClose, \
                         MDT_adjClose, \
                         MET_adjClose, \
                         MGM_adjClose, \
                         MHK_adjClose, \
                         MKC_adjClose \
                         MKTX_adjClose, \
                         MLM_adjClose, \
                         MMC_adjClose, \
                         MMI_adjClose, \
                         MMM_adjClose, \
                         MNST_adjClose, \
                         MO_adjClose, \
                         MOH_adjClose, \
                         MOS_adjClose, \
                         MPC_adjClose, \
                         MPWR_adjClose, \
                         MRK_adjClose, \
                         MRO_adjClose, \
                         MRVL_adjClose, \
                         MS_adjClose, \
                         MSCI_adjClose, \
                         MSFT_adjClose, \
                         MSI_adjClose, \
                         MTB_adjClose, \
                         MTCH_adjClose, \
                         MTD_adjClose, \
                         MTW_adjClose, \
                         MU_adjClose, \
                         MUR_adjClose, \
                         NAVI_adjClose, \
                         NBR_adjClose, \
                         NCLH_adjClose, \
                         NDAQ_adjClose, \
                         NDSN_adjClose, \
                         NE_adjClose, \
                         NEE_adjClose, \
                         NEM_adjClose, \
                         NFLX_adjClose, \
                         NI_adjClose, \
                         NKE_adjClose, \
                         NKTR_adjClose, \
                         NLOK_adjClose, \
                         NLSN_adjClose, \
                         NOC_adjClose, \
                         NOV_adjClose, \
                         NOW_adjClose, \
                         NRG_adjClose, \
                         NSC_adjClose, \
                         NTAP_adjClose, \
                         NTES_adjClose, \
                         NTRS_adjClose, \
                         NUE_adjClose, \
                         NVDA_adjClose, \
                         NVR_adjClose, \
                         NWL_adjClose, \
                         NWS_adjClose, \
                         NWSA_adjClose, \
                         NXPI_adjClose, \
                         NYT_adjClose, \
                         O_adjClose, \
                         ODFL_adjClose, \
                         ODP_adjClose, \
                         OGN_adjClose, \
                         OI_adjClose, \
                         OKE_adjClose, \
                         OMC_adjClose, \
                         ONE_adjClose, \
                         ORCL_adjClose, \
                         ORLY_adjClose, \
                         OTIS_adjClose, \
                         OXY_adjClose, \
                         PAR_adjClose, \
                         PAYC_adjClose, \
                         PAYX_adjClose, \
                         PBCT_adjClose \
                         PBI_adjClose, \
                         PCAR_adjClose, \
                         PCG_adjClose, \
                         PDCO_adjClose, \
                         PEAK_adjClose, \
                         PEG_adjClose, \
                         PENN_adjClose, \
                         PEP_adjClose, \
                         PFE_adjClose, \
                         PFG_adjClose, \
                         PG_adjClose, \
                         PGR_adjClose, \
                         PH_adjClose, \
                         PHM_adjClose, \
                         PKG_adjClose, \
                         PKI_adjClose, \
                         PLD_adjClose, \
                         PLL_adjClose, \
                         PM_adjClose, \
                         PNC_adjClose, \
                         PNR_adjClose, \
                         PNW_adjClose, \
                         POOL_adjClose, \
                         PPG_adjClose, \
                         PPL_adjClose, \
                         PRGO_adjClose, \
                         PRI_adjClose, \
                         PRU_adjClose, \
                         PSA_adjClose, \
                         PSX_adjClose, \
                         PTC_adjClose, \
                         PVH_adjClose, \
                         PWR_adjClose, \
                         PXD_adjClose, \
                         PYPL_adjClose, \
                         QCOM_adjClose, \
                         QGEN_adjClose, \
                         QRVO_adjClose, \
          FROM deltabase.aapl_30min_delta \
     FULL JOIN deltabase.aa_30min_delta ON aapl_30min_delta.AAPL_dateTime = AA_dateTime \
     FULL JOIN deltabase.aal_30min_delta ON aapl_30min_delta.AAPL_dateTime = AAL_dateTime \
     FULL JOIN deltabase.aap_30min_delta ON aapl_30min_delta.AAPL_dateTime = AAP_dateTime \
     FULL JOIN deltabase.a_30min_delta ON aapl_30min_delta.AAPL_dateTime = A_dateTime \
     FULL JOIN deltabase.abbv_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABBV_dateTime \
     FULL JOIN deltabase.abc_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABC_dateTime \
     FULL JOIN deltabase.abmd_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABMD_dateTime \
     FULL JOIN deltabase.abt_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABT_dateTime \
     FULL JOIN deltabase.acn_30min_delta ON aapl_30min_delta.AAPL_dateTime = ACN_dateTime \
     FULL JOIN deltabase.acv_30min_delta ON aapl_30min_delta.AAPL_dateTime = ACV_dateTime \
     FULL JOIN deltabase.adbe_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADBE_dateTime \
     FULL JOIN deltabase.adi_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADI_dateTime \
     FULL JOIN deltabase.adm_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADM_dateTime \
     FULL JOIN deltabase.adp_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADP_dateTime \
     FULL JOIN deltabase.ads_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADS_dateTime \
     FULL JOIN deltabase.adsk_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADSK_dateTime \
     FULL JOIN deltabase.adt_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADT_dateTime \
     FULL JOIN deltabase.aee_30min_delta ON aapl_30min_delta.AAPL_dateTime = AEE_dateTime \
     FULL JOIN deltabase.aep_30min_delta ON aapl_30min_delta.AAPL_dateTime = AEP_dateTime \
     FULL JOIN deltabase.aes_30min_delta ON aapl_30min_delta.AAPL_dateTime = AES_dateTime \
     FULL JOIN deltabase.afl_30min_delta ON aapl_30min_delta.AAPL_dateTime = AFL_dateTime \
     FULL JOIN deltabase.aig_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIG_dateTime \
     FULL JOIN deltabase.ainv_30min_delta ON aapl_30min_delta.AAPL_dateTime = AINV_dateTime \
     FULL JOIN deltabase.aiv_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIV_dateTime \
     FULL JOIN deltabase.aiz_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIZ_dateTime \
     FULL JOIN deltabase.ajg_30min_delta ON aapl_30min_delta.AAPL_dateTime = AJG_dateTime \
     FULL JOIN deltabase.akam_30min_delta ON aapl_30min_delta.AAPL_dateTime = AKAM_dateTime \
     FULL JOIN deltabase.alb_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALB_dateTime \
     FULL JOIN deltabase.algn_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALGN_dateTime \
     FULL JOIN deltabase.alk_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALK_dateTime \
     FULL JOIN deltabase.all_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALL_dateTime \
     FULL JOIN deltabase.alle_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALLE_dateTime \
     FULL JOIN deltabase.altr_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALTR_dateTime \
     FULL JOIN deltabase.amat_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMAT_dateTime \
     FULL JOIN deltabase.ambc_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMBC_dateTime \
     FULL JOIN deltabase.amcr_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMCR_dateTime \
     FULL JOIN deltabase.amd_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMD_dateTime \
     FULL JOIN deltabase.ame_30min_delta ON aapl_30min_delta.AAPL_dateTime = AME_dateTime \
     FULL JOIN deltabase.amg_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMG_dateTime \
     FULL JOIN deltabase.amgn_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMGN_dateTime \
     FULL JOIN deltabase.amp_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMP_dateTime \
     FULL JOIN deltabase.amt_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMT_dateTime \
     FULL JOIN deltabase.amzn_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMZN_dateTime \
     FULL JOIN deltabase.an_30min_delta ON aapl_30min_delta.AAPL_dateTime = AN_dateTime \
     FULL JOIN deltabase.anet_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANET_dateTime \
     FULL JOIN deltabase.anf_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANF_dateTime \
     FULL JOIN deltabase.anss_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANSS_dateTime \
     FULL JOIN deltabase.antm_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANTM_dateTime \
     FULL JOIN deltabase.aon_30min_delta ON aapl_30min_delta.AAPL_dateTime = AON_dateTime \
     FULL JOIN deltabase.aos_30min_delta ON aapl_30min_delta.AAPL_dateTime = AOS_dateTime \
     FULL JOIN deltabase.apa_30min_delta ON aapl_30min_delta.AAPL_dateTime = APA_dateTime \
     FULL JOIN deltabase.apd_30min_delta ON aapl_30min_delta.AAPL_dateTime = APD_dateTime \
     FULL JOIN deltabase.aph_30min_delta ON aapl_30min_delta.AAPL_dateTime = APH_dateTime \
     FULL JOIN deltabase.aptv_30min_delta ON aapl_30min_delta.AAPL_dateTime = APTV_dateTime \
     FULL JOIN deltabase.are_30min_delta ON aapl_30min_delta.AAPL_dateTime = ARE_dateTime \
     FULL JOIN deltabase.arnc_30min_delta ON aapl_30min_delta.AAPL_dateTime = ARNC_dateTime \
     FULL JOIN deltabase.ash_30min_delta ON aapl_30min_delta.AAPL_dateTime = ASH_dateTime \
     FULL JOIN deltabase.aso_30min_delta ON aapl_30min_delta.AAPL_dateTime = ASO_dateTime \
     FULL JOIN deltabase.atge_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATGE_dateTime \
     FULL JOIN deltabase.ati_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATI_dateTime \
     FULL JOIN deltabase.ato_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATO_dateTime \
     FULL JOIN deltabase.atvi_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATVI_dateTime \
     FULL JOIN deltabase.avb_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVB_dateTime \
     FULL JOIN deltabase.avgo_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVGO_dateTime \
     FULL JOIN deltabase.avy_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVY_dateTime \
     FULL JOIN deltabase.awk_30min_delta ON aapl_30min_delta.AAPL_dateTime = AWK_dateTime \
     FULL JOIN deltabase.axp_30min_delta ON aapl_30min_delta.AAPL_dateTime = AXP_dateTime \
     FULL JOIN deltabase.ayi_30min_delta ON aapl_30min_delta.AAPL_dateTime = AYI_dateTime \
     FULL JOIN deltabase.azo_30min_delta ON aapl_30min_delta.AAPL_dateTime = AZO_dateTime \
     FULL JOIN deltabase.ba_30min_delta ON aapl_30min_delta.AAPL_dateTime = BA_dateTime \
     FULL JOIN deltabase.bac_30min_delta ON aapl_30min_delta.AAPL_dateTime = BAC_dateTime \
     FULL JOIN deltabase.bax_30min_delta ON aapl_30min_delta.AAPL_dateTime = BAX_dateTime \
     FULL JOIN deltabase.bbby_30min_delta ON aapl_30min_delta.AAPL_dateTime = BBBY_dateTime \
     FULL JOIN deltabase.bby_30min_delta ON aapl_30min_delta.AAPL_dateTime = BBY_dateTime \
     FULL JOIN deltabase.bc_30min_delta ON aapl_30min_delta.AAPL_dateTime = BC_dateTime \
     FULL JOIN deltabase.bdx_30min_delta ON aapl_30min_delta.AAPL_dateTime = BDX_dateTime \
     FULL JOIN deltabase.ben_30min_delta ON aapl_30min_delta.AAPL_dateTime = BEN_dateTime \
     FULL JOIN deltabase.bfb_30min_delta ON aapl_30min_delta.AAPL_dateTime = BFB_dateTime \
     FULL JOIN deltabase.bidu_30min_delta ON aapl_30min_delta.AAPL_dateTime = BIDU_dateTime \
     FULL JOIN deltabase.big_30min_delta ON aapl_30min_delta.AAPL_dateTime = BIG_dateTime \
     FULL JOIN deltabase.biib_30min_delta ON aapl_30min_delta.AAPL_dateTime = BIIB_dateTime \
     FULL JOIN deltabase.bio_30min_delta ON aapl_30min_delta.AAPL_dateTime = BIO_dateTime \
     FULL JOIN deltabase.bk_30min_delta ON aapl_30min_delta.AAPL_dateTime = BK_dateTime \
     FULL JOIN deltabase.bkng_30min_delta ON aapl_30min_delta.AAPL_dateTime = BKNG_dateTime \
     FULL JOIN deltabase.blk_30min_delta ON aapl_30min_delta.AAPL_dateTime = BLK_dateTime \
     FULL JOIN deltabase.bll_30min_delta ON aapl_30min_delta.AAPL_dateTime = BLL_dateTime \
     FULL JOIN deltabase.bmrn_30min_delta ON aapl_30min_delta.AAPL_dateTime = BMRN_dateTime \
     FULL JOIN deltabase.bmy_30min_delta ON aapl_30min_delta.AAPL_dateTime = BMY_dateTime \
     FULL JOIN deltabase.br_30min_delta ON aapl_30min_delta.AAPL_dateTime = BR_dateTime \
     FULL JOIN deltabase.brkb_30min_delta ON aapl_30min_delta.AAPL_dateTime = BRKB_dateTime \
     FULL JOIN deltabase.bro_30min_delta ON aapl_30min_delta.AAPL_dateTime = BRO_dateTime \
     FULL JOIN deltabase.bsx_30min_delta ON aapl_30min_delta.AAPL_dateTime = BSX_dateTime \
     FULL JOIN deltabase.btu_30min_delta ON aapl_30min_delta.AAPL_dateTime = BTU_dateTime \
     FULL JOIN deltabase.bud_30min_delta ON aapl_30min_delta.AAPL_dateTime = BUD_dateTime \
     FULL JOIN deltabase.bwa_30min_delta ON aapl_30min_delta.AAPL_dateTime = BWA_dateTime \
     FULL JOIN deltabase.bxp_30min_delta ON aapl_30min_delta.AAPL_dateTime = BXP_dateTime \
     FULL JOIN deltabase.c_30min_delta ON aapl_30min_delta.AAPL_dateTime = C_dateTime \
     FULL JOIN deltabase.cag_30min_delta ON aapl_30min_delta.AAPL_dateTime = CAG_dateTime \
     FULL JOIN deltabase.cah_30min_delta ON aapl_30min_delta.AAPL_dateTime = CAH_dateTime \
     FULL JOIN deltabase.car_30min_delta ON aapl_30min_delta.AAPL_dateTime = CAR_dateTime \
     FULL JOIN deltabase.carr_30min_delta ON aapl_30min_delta.AAPL_dateTime = CARR_dateTime \
     FULL JOIN deltabase.cat_30min_delta ON aapl_30min_delta.AAPL_dateTime = CAT_dateTime \
     FULL JOIN deltabase.cb_30min_delta ON aapl_30min_delta.AAPL_dateTime = CB_dateTime \
     FULL JOIN deltabase.cbh_30min_delta ON aapl_30min_delta.AAPL_dateTime = CBH_dateTime \
     FULL JOIN deltabase.cboe_30min_delta ON aapl_30min_delta.AAPL_dateTime = CBOE_dateTime \
     FULL JOIN deltabase.cbre_30min_delta ON aapl_30min_delta.AAPL_dateTime = CBRE_dateTime \
     FULL JOIN deltabase.cc_30min_delta ON aapl_30min_delta.AAPL_dateTime = CC_dateTime \
     FULL JOIN deltabase.cci_30min_delta ON aapl_30min_delta.AAPL_dateTime = CCI_dateTime \
     FULL JOIN deltabase.cck_30min_delta ON aapl_30min_delta.AAPL_dateTime = CCK_dateTime \
     FULL JOIN deltabase.ccl_30min_delta ON aapl_30min_delta.AAPL_dateTime = CCL_dateTime \
     FULL JOIN deltabase.ccu_30min_delta ON aapl_30min_delta.AAPL_dateTime = CCU_dateTime \
     FULL JOIN deltabase.cday_30min_delta ON aapl_30min_delta.AAPL_dateTime = CDAY_dateTime \
     FULL JOIN deltabase.cdns_30min_delta ON aapl_30min_delta.AAPL_dateTime = CDNS_dateTime \
     FULL JOIN deltabase.cdw_30min_delta ON aapl_30min_delta.AAPL_dateTime = CDW_dateTime \
     FULL JOIN deltabase.ce_30min_delta ON aapl_30min_delta.AAPL_dateTime = CE_dateTime \
     FULL JOIN deltabase.cern_30min_delta ON aapl_30min_delta.AAPL_dateTime = CERN_dateTime \
     FULL JOIN deltabase.cf_30min_delta ON aapl_30min_delta.AAPL_dateTime = CF_dateTime \
     FULL JOIN deltabase.cfg_30min_delta ON aapl_30min_delta.AAPL_dateTime = CFG_dateTime \
     FULL JOIN deltabase.chd_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHD_dateTime \
     FULL JOIN deltabase.chir_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHIR_dateTime \
     FULL JOIN deltabase.chk_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHK_dateTime \
     FULL JOIN deltabase.chkp_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHKP_dateTime \
     FULL JOIN deltabase.chrw_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHRW_dateTime \
     FULL JOIN deltabase.chtr_30min_delta ON aapl_30min_delta.AAPL_dateTime = CHTR_dateTime \
     FULL JOIN deltabase.ci_30min_delta ON aapl_30min_delta.AAPL_dateTime = CI_dateTime \
     FULL JOIN deltabase.cien_30min_delta ON aapl_30min_delta.AAPL_dateTime = CIEN_dateTime \
     FULL JOIN deltabase.cinf_30min_delta ON aapl_30min_delta.AAPL_dateTime = CINF_dateTime \
     FULL JOIN deltabase.cit_30min_delta ON aapl_30min_delta.AAPL_dateTime = CIT_dateTime \
     FULL JOIN deltabase.cl_30min_delta ON aapl_30min_delta.AAPL_dateTime = CL_dateTime \
     FULL JOIN deltabase.clf_30min_delta ON aapl_30min_delta.AAPL_dateTime = CLF_dateTime \
     FULL JOIN deltabase.clx_30min_delta ON aapl_30min_delta.AAPL_dateTime = CLX_dateTime \
     FULL JOIN deltabase.cma_30min_delta ON aapl_30min_delta.AAPL_dateTime = CMA_dateTime \
     FULL JOIN deltabase.cmcsa_30min_delta ON aapl_30min_delta.AAPL_dateTime = CMCSA_dateTime \
     FULL JOIN deltabase.cme_30min_delta ON aapl_30min_delta.AAPL_dateTime = CME_dateTime \
     FULL JOIN deltabase.cmg_30min_delta ON aapl_30min_delta.AAPL_dateTime = CMG_dateTime \
     FULL JOIN deltabase.cmi_30min_delta ON aapl_30min_delta.AAPL_dateTime = CMI_dateTime \
     FULL JOIN deltabase.cms_30min_delta ON aapl_30min_delta.AAPL_dateTime = CMS_dateTime \
     FULL JOIN deltabase.cnc_30min_delta ON aapl_30min_delta.AAPL_dateTime = CNC_dateTime \
     FULL JOIN deltabase.cnp_30min_delta ON aapl_30min_delta.AAPL_dateTime = CNP_dateTime \
     FULL JOIN deltabase.cnx_30min_delta ON aapl_30min_delta.AAPL_dateTime = CNX_dateTime \
     FULL JOIN deltabase.cof_30min_delta ON aapl_30min_delta.AAPL_dateTime = COF_dateTime \
     FULL JOIN deltabase.coo_30min_delta ON aapl_30min_delta.AAPL_dateTime = COO_dateTime \
     FULL JOIN deltabase.coop_30min_delta ON aapl_30min_delta.AAPL_dateTime = COOP_dateTime \
     FULL JOIN deltabase.cop_30min_delta ON aapl_30min_delta.AAPL_dateTime = COP_dateTime \
     FULL JOIN deltabase.cost_30min_delta ON aapl_30min_delta.AAPL_dateTime = COST_dateTime \
     FULL JOIN deltabase.coty_30min_delta ON aapl_30min_delta.AAPL_dateTime = COTY_dateTime \
     FULL JOIN deltabase.cpb_30min_delta ON aapl_30min_delta.AAPL_dateTime = CPB_dateTime \
     FULL JOIN deltabase.cpri_30min_delta ON aapl_30min_delta.AAPL_dateTime = CPRI_dateTime \
     FULL JOIN deltabase.cprt_30min_delta ON aapl_30min_delta.AAPL_dateTime = CPRT_dateTime \
     FULL JOIN deltabase.cpt_30min_delta ON aapl_30min_delta.AAPL_dateTime = CPT_dateTime \
     FULL JOIN deltabase.crm_30min_delta ON aapl_30min_delta.AAPL_dateTime = CRM_dateTime \
     FULL JOIN deltabase.csco_30min_delta ON aapl_30min_delta.AAPL_dateTime = CSCO_dateTime \
     FULL JOIN deltabase.csx_30min_delta ON aapl_30min_delta.AAPL_dateTime = CSX_dateTime \
     FULL JOIN deltabase.ctas_30min_delta ON aapl_30min_delta.AAPL_dateTime = CTAS_dateTime \
     FULL JOIN deltabase.ctlt_30min_delta ON aapl_30min_delta.AAPL_dateTime = CTLT_dateTime \
     FULL JOIN deltabase.ctsh_30min_delta ON aapl_30min_delta.AAPL_dateTime = CTSH_dateTime \
     FULL JOIN deltabase.ctva_30min_delta ON aapl_30min_delta.AAPL_dateTime = CTVA_dateTime \
     FULL JOIN deltabase.ctxs_30min_delta ON aapl_30min_delta.AAPL_dateTime = CTXS_dateTime \
     FULL JOIN deltabase.cvs_30min_delta ON aapl_30min_delta.AAPL_dateTime = CVS_dateTime \
     FULL JOIN deltabase.cvx_30min_delta ON aapl_30min_delta.AAPL_dateTime = CVX_dateTime \
     FULL JOIN deltabase.czr_30min_delta ON aapl_30min_delta.AAPL_dateTime = CZR_dateTime \
     FULL JOIN deltabase.d_30min_delta ON aapl_30min_delta.AAPL_dateTime = D_dateTime \
     FULL JOIN deltabase.dal_30min_delta ON aapl_30min_delta.AAPL_dateTime = DAL_dateTime \
     FULL JOIN deltabase.dan_30min_delta ON aapl_30min_delta.AAPL_dateTime = DAN_dateTime \
     FULL JOIN deltabase.dd_30min_delta ON aapl_30min_delta.AAPL_dateTime = DD_dateTime \
     FULL JOIN deltabase.dds_30min_delta ON aapl_30min_delta.AAPL_dateTime = DDS_dateTime \
     FULL JOIN deltabase.de_30min_delta ON aapl_30min_delta.AAPL_dateTime = DE_dateTime \
     FULL JOIN deltabase.dell_30min_delta ON aapl_30min_delta.AAPL_dateTime = DELL_dateTime \
     FULL JOIN deltabase.dfs_30min_delta ON aapl_30min_delta.AAPL_dateTime = DFS_dateTime \
     FULL JOIN deltabase.dg_30min_delta ON aapl_30min_delta.AAPL_dateTime = DG_dateTime \
     FULL JOIN deltabase.dgx_30min_delta ON aapl_30min_delta.AAPL_dateTime = DGX_dateTime \
     FULL JOIN deltabase.dhi_30min_delta ON aapl_30min_delta.AAPL_dateTime = DHI_dateTime \
     FULL JOIN deltabase.dhr_30min_delta ON aapl_30min_delta.AAPL_dateTime = DHR_dateTime \
     FULL JOIN deltabase.dis_30min_delta ON aapl_30min_delta.AAPL_dateTime = DIS_dateTime \
     FULL JOIN deltabase.disca_30min_delta ON aapl_30min_delta.AAPL_dateTime = DISCA_dateTime \
     FULL JOIN deltabase.disck_30min_delta ON aapl_30min_delta.AAPL_dateTime = DISCK_dateTime \
     FULL JOIN deltabase.dish_30min_delta ON aapl_30min_delta.AAPL_dateTime = DISH_dateTime \
     FULL JOIN deltabase.dlr_30min_delta ON aapl_30min_delta.AAPL_dateTime = DLR_dateTime \
     FULL JOIN deltabase.dltr_30min_delta ON aapl_30min_delta.AAPL_dateTime = DLTR_dateTime \
     FULL JOIN deltabase.dlx_30min_delta ON aapl_30min_delta.AAPL_dateTime = DLX_dateTime \
     FULL JOIN deltabase.dnb_30min_delta ON aapl_30min_delta.AAPL_dateTime = DNB_dateTime \
     FULL JOIN deltabase.dov_30min_delta ON aapl_30min_delta.AAPL_dateTime = DOV_dateTime \
     FULL JOIN deltabase.dow_30min_delta ON aapl_30min_delta.AAPL_dateTime = DOW_dateTime \
     FULL JOIN deltabase.dpz_30min_delta ON aapl_30min_delta.AAPL_dateTime = DPZ_dateTime \
     FULL JOIN deltabase.dre_30min_delta ON aapl_30min_delta.AAPL_dateTime = DRE_dateTime \
     FULL JOIN deltabase.dri_30min_delta ON aapl_30min_delta.AAPL_dateTime = DRI_dateTime \
     FULL JOIN deltabase.dte_30min_delta ON aapl_30min_delta.AAPL_dateTime = DTE_dateTime \
     FULL JOIN deltabase.duk_30min_delta ON aapl_30min_delta.AAPL_dateTime = DUK_dateTime \
     FULL JOIN deltabase.dva_30min_delta ON aapl_30min_delta.AAPL_dateTime = DVA_dateTime \
     FULL JOIN deltabase.dvn_30min_delta ON aapl_30min_delta.AAPL_dateTime = DVN_dateTime \
     FULL JOIN deltabase.dxc_30min_delta ON aapl_30min_delta.AAPL_dateTime = DXC_dateTime \
     FULL JOIN deltabase.dxcm_30min_delta ON aapl_30min_delta.AAPL_dateTime = DXCM_dateTime \
     FULL JOIN deltabase.EA_30min_delta ON aapl_30min_delta.AAPL_dateTime = EA_dateTime \
     FULL JOIN deltabase.EBAY_30min_delta ON aapl_30min_delta.AAPL_dateTime = EBAY_dateTime \
     FULL JOIN deltabase.ECL_30min_delta ON aapl_30min_delta.AAPL_dateTime = ECL_dateTime \
     FULL JOIN deltabase.ED_30min_delta ON aapl_30min_delta.AAPL_dateTime = ED_dateTime \
     FULL JOIN deltabase.EFX_30min_delta ON aapl_30min_delta.AAPL_dateTime = EFX_dateTime \
     FULL JOIN deltabase.EIX_30min_delta ON aapl_30min_delta.AAPL_dateTime = EIX_dateTime \
     FULL JOIN deltabase.EL_30min_delta ON aapl_30min_delta.AAPL_dateTime = EL_dateTime \
     FULL JOIN deltabase.EMN_30min_delta ON aapl_30min_delta.AAPL_dateTime = EMN_dateTime \
     FULL JOIN deltabase.EMR_30min_delta ON aapl_30min_delta.AAPL_dateTime = EMR_dateTime \
     FULL JOIN deltabase.ENDP_30min_delta ON aapl_30min_delta.AAPL_dateTime = ENDP_dateTime \
     FULL JOIN deltabase.ENPH_30min_delta ON aapl_30min_delta.AAPL_dateTime = ENPH_dateTime \
     FULL JOIN deltabase.EOG_30min_delta ON aapl_30min_delta.AAPL_dateTime = EOG_dateTime \
     FULL JOIN deltabase.EPAM_30min_delta ON aapl_30min_delta.AAPL_dateTime = EPAM_dateTime \
     FULL JOIN deltabase.EQ_30min_delta ON aapl_30min_delta.AAPL_dateTime = EQ_dateTime \
     FULL JOIN deltabase.EQIX_30min_delta ON aapl_30min_delta.AAPL_dateTime = EQIX_dateTime \
     FULL JOIN deltabase.EQR_30min_delta ON aapl_30min_delta.AAPL_dateTime = EQR_dateTime \
     FULL JOIN deltabase.EQT_30min_delta ON aapl_30min_delta.AAPL_dateTime = EQT_dateTime \
     FULL JOIN deltabase.ES_30min_delta ON aapl_30min_delta.AAPL_dateTime = ES_dateTime \
     FULL JOIN deltabase.ESS_30min_delta ON aapl_30min_delta.AAPL_dateTime = ESS_dateTime \
     FULL JOIN deltabase.ETN_30min_delta ON aapl_30min_delta.AAPL_dateTime = ETN_dateTime \
     FULL JOIN deltabase.ETR_30min_delta ON aapl_30min_delta.AAPL_dateTime = ETR_dateTime \
     FULL JOIN deltabase.ETSY_30min_delta ON aapl_30min_delta.AAPL_dateTime = ETSY_dateTime \
     FULL JOIN deltabase.EVRG_30min_delta ON aapl_30min_delta.AAPL_dateTime = EVRG_dateTime \
     FULL JOIN deltabase.EW_30min_delta ON aapl_30min_delta.AAPL_dateTime = EW_dateTime \
     FULL JOIN deltabase.EXC_30min_delta ON aapl_30min_delta.AAPL_dateTime = EXC_dateTime \
     FULL JOIN deltabase.EXPD_30min_delta ON aapl_30min_delta.AAPL_dateTime = EXPD_dateTime \
     FULL JOIN deltabase.EXPE_30min_delta ON aapl_30min_delta.AAPL_dateTime = EXPE_dateTime \
     FULL JOIN deltabase.EXR_30min_delta ON aapl_30min_delta.AAPL_dateTime = EXR_dateTime \
     FULL JOIN deltabase.F_30min_delta ON aapl_30min_delta.AAPL_dateTime = F_dateTime \
     FULL JOIN deltabase.FANG_30min_delta ON aapl_30min_delta.AAPL_dateTime = FANG_dateTime \
     FULL JOIN deltabase.FAST_30min_delta ON aapl_30min_delta.AAPL_dateTime = FAST_dateTime \
     FULL JOIN deltabase.FB_30min_delta ON aapl_30min_delta.AAPL_dateTime = FB_dateTime \
     FULL JOIN deltabase.FBHS_30min_delta ON aapl_30min_delta.AAPL_dateTime = FBHS_dateTime \
     FULL JOIN deltabase.FCX_30min_delta ON aapl_30min_delta.AAPL_dateTime = FCX_dateTime \
     FULL JOIN deltabase.FDS_30min_delta ON aapl_30min_delta.AAPL_dateTime = FDS_dateTime \
     FULL JOIN deltabase.FDX_30min_delta ON aapl_30min_delta.AAPL_dateTime = FDX_dateTime \
     FULL JOIN deltabase.FE_30min_delta ON aapl_30min_delta.AAPL_dateTime = FE_dateTime \
     FULL JOIN deltabase.FFIV_30min_delta ON aapl_30min_delta.AAPL_dateTime = FFIV_dateTime \
     FULL JOIN deltabase.FHN_30min_delta ON aapl_30min_delta.AAPL_dateTime = FHN_dateTime \
     FULL JOIN deltabase.FIS_30min_delta ON aapl_30min_delta.AAPL_dateTime = FIS_dateTime \
     FULL JOIN deltabase.FISV_30min_delta ON aapl_30min_delta.AAPL_dateTime = FISV_dateTime \
     FULL JOIN deltabase.FITB_30min_delta ON aapl_30min_delta.AAPL_dateTime = FITB_dateTime \
     FULL JOIN deltabase.FL_30min_delta ON aapl_30min_delta.AAPL_dateTime = FL_dateTime \
     FULL JOIN deltabase.FLEX_30min_delta ON aapl_30min_delta.AAPL_dateTime = FLEX_dateTime \
     FULL JOIN deltabase.FLR_30min_delta ON aapl_30min_delta.AAPL_dateTime = FLR_dateTime \
     FULL JOIN deltabase.FLS_30min_delta ON aapl_30min_delta.AAPL_dateTime = FLS_dateTime \
     FULL JOIN deltabase.FLT_30min_delta ON aapl_30min_delta.AAPL_dateTime = FLT_dateTime \
     FULL JOIN deltabase.FMC_30min_delta ON aapl_30min_delta.AAPL_dateTime = FMC_dateTime \
     FULL JOIN deltabase.FOSL_30min_delta ON aapl_30min_delta.AAPL_dateTime = FOSL_dateTime \
     FULL JOIN deltabase.FOX_30min_delta ON aapl_30min_delta.AAPL_dateTime = FOX_dateTime \
     FULL JOIN deltabase.FOXA_30min_delta ON aapl_30min_delta.AAPL_dateTime = FOXA_dateTime \
     FULL JOIN deltabase.FPL_30min_delta ON aapl_30min_delta.AAPL_dateTime = FPL_dateTime \
     FULL JOIN deltabase.FRC_30min_delta ON aapl_30min_delta.AAPL_dateTime = FRC_dateTime \
     FULL JOIN deltabase.FRT_30min_delta ON aapl_30min_delta.AAPL_dateTime = FRT_dateTime \
     FULL JOIN deltabase.FSLR_30min_delta ON aapl_30min_delta.AAPL_dateTime = FSLR_dateTime \
     FULL JOIN deltabase.FTI_30min_delta ON aapl_30min_delta.AAPL_dateTime = FTI_dateTime \
     FULL JOIN deltabase.FTNT_30min_delta ON aapl_30min_delta.AAPL_dateTime = FTNT_dateTime \
     FULL JOIN deltabase.FTV_30min_delta ON aapl_30min_delta.AAPL_dateTime = FTV_dateTime \
     FULL JOIN deltabase.GCI_30min_delta ON aapl_30min_delta.AAPL_dateTime = GCI_dateTime \
     FULL JOIN deltabase.GD_30min_delta ON aapl_30min_delta.AAPL_dateTime = GD_dateTime \
     FULL JOIN deltabase.GE_30min_delta ON aapl_30min_delta.AAPL_dateTime = GE_dateTime \
     FULL JOIN deltabase.GHC_30min_delta ON aapl_30min_delta.AAPL_dateTime = GHC_dateTime \
     FULL JOIN deltabase.GILD_30min_delta ON aapl_30min_delta.AAPL_dateTime = GILD_dateTime \
     FULL JOIN deltabase.GIS_30min_delta ON aapl_30min_delta.AAPL_dateTime = GIS_dateTime \
     FULL JOIN deltabase.GL_30min_delta ON aapl_30min_delta.AAPL_dateTime = GL_dateTime \
     FULL JOIN deltabase.GLW_30min_delta ON aapl_30min_delta.AAPL_dateTime = GLW_dateTime \
     FULL JOIN deltabase.GM_30min_delta ON aapl_30min_delta.AAPL_dateTime = GM_dateTime \
     FULL JOIN deltabase.GME_30min_delta ON aapl_30min_delta.AAPL_dateTime = GME_dateTime \
     FULL JOIN deltabase.GNRC_30min_delta ON aapl_30min_delta.AAPL_dateTime = GNRC_dateTime \
     FULL JOIN deltabase.GNW_30min_delta ON aapl_30min_delta.AAPL_dateTime = GNW_dateTime \
     FULL JOIN deltabase.GOOG_30min_delta ON aapl_30min_delta.AAPL_dateTime = GOOG_dateTime \
     FULL JOIN deltabase.GOOGL_30min_delta ON aapl_30min_delta.AAPL_dateTime = GOOGL_dateTime \
     FULL JOIN deltabase.GP_30min_delta ON aapl_30min_delta.AAPL_dateTime = GP_dateTime \
     FULL JOIN deltabase.GPC_30min_delta ON aapl_30min_delta.AAPL_dateTime = GPC_dateTime \
     FULL JOIN deltabase.GPN_30min_delta ON aapl_30min_delta.AAPL_dateTime = GPN_dateTime \
     FULL JOIN deltabase.GPS_30min_delta ON aapl_30min_delta.AAPL_dateTime = GPS_dateTime \
     FULL JOIN deltabase.GRMN_30min_delta ON aapl_30min_delta.AAPL_dateTime = GRMN_dateTime \
     FULL JOIN deltabase.GS_30min_delta ON aapl_30min_delta.AAPL_dateTime = GS_dateTime \
     FULL JOIN deltabase.GT_30min_delta ON aapl_30min_delta.AAPL_dateTime = GT_dateTime \
     FULL JOIN deltabase.GWW_30min_delta ON aapl_30min_delta.AAPL_dateTime = GWW_dateTime \
     FULL JOIN deltabase.HAL_30min_delta ON aapl_30min_delta.AAPL_dateTime = HAL_dateTime \
     FULL JOIN deltabase.HAS_30min_delta ON aapl_30min_delta.AAPL_dateTime = HAS_dateTime \
     FULL JOIN deltabase.HBAN_30min_delta ON aapl_30min_delta.AAPL_dateTime = HBAN_dateTime \
     FULL JOIN deltabase.HBI_30min_delta ON aapl_30min_delta.AAPL_dateTime = HBI_dateTime \
     FULL JOIN deltabase.HCA_30min_delta ON aapl_30min_delta.AAPL_dateTime = HCA_dateTime \
     FULL JOIN deltabase.HD_30min_delta ON aapl_30min_delta.AAPL_dateTime = HD_dateTime \
     FULL JOIN deltabase.HES_30min_delta ON aapl_30min_delta.AAPL_dateTime = HES_dateTime \
     FULL JOIN deltabase.HFC_30min_delta ON aapl_30min_delta.AAPL_dateTime = HFC_dateTime \
     FULL JOIN deltabase.HIG_30min_delta ON aapl_30min_delta.AAPL_dateTime = HIG_dateTime \
     FULL JOIN deltabase.HII_30min_delta ON aapl_30min_delta.AAPL_dateTime = HII_dateTime \
     FULL JOIN deltabase.HLT_30min_delta ON aapl_30min_delta.AAPL_dateTime = HLT_dateTime \
     FULL JOIN deltabase.HOG_30min_delta ON aapl_30min_delta.AAPL_dateTime = HOG_dateTime \
     FULL JOIN deltabase.HOLX_30min_delta ON aapl_30min_delta.AAPL_dateTime = HOLX_dateTime \
     FULL JOIN deltabase.HON_30min_delta ON aapl_30min_delta.AAPL_dateTime = HON_dateTime \
     FULL JOIN deltabase.HP_30min_delta ON aapl_30min_delta.AAPL_dateTime = HP_dateTime \
     FULL JOIN deltabase.HPE_30min_delta ON aapl_30min_delta.AAPL_dateTime = HPE_dateTime \
     FULL JOIN deltabase.HPQ_30min_delta ON aapl_30min_delta.AAPL_dateTime = HPQ_dateTime \
     FULL JOIN deltabase.HRB_30min_delta ON aapl_30min_delta.AAPL_dateTime = HRB_dateTime \
     FULL JOIN deltabase.HRL_30min_delta ON aapl_30min_delta.AAPL_dateTime = HRL_dateTime \
     FULL JOIN deltabase.HSIC_30min_delta ON aapl_30min_delta.AAPL_dateTime = HSIC_dateTime \
     FULL JOIN deltabase.HST_30min_delta ON aapl_30min_delta.AAPL_dateTime = HST_dateTime \
     FULL JOIN deltabase.HSY_30min_delta ON aapl_30min_delta.AAPL_dateTime = HSY_dateTime \
     FULL JOIN deltabase.HUM_30min_delta ON aapl_30min_delta.AAPL_dateTime = HUM_dateTime \
     FULL JOIN deltabase.IAC_30min_delta ON aapl_30min_delta.AAPL_dateTime = IAC_dateTime \
     FULL JOIN deltabase.IBM_30min_delta ON aapl_30min_delta.AAPL_dateTime = IBM_dateTime \
     FULL JOIN deltabase.ICE_30min_delta ON aapl_30min_delta.AAPL_dateTime = ICE_dateTime \
     FULL JOIN deltabase.IDXX_30min_delta ON aapl_30min_delta.AAPL_dateTime = IDXX_dateTime \
     FULL JOIN deltabase.IEX_30min_delta ON aapl_30min_delta.AAPL_dateTime = IEX_dateTime \
     FULL JOIN deltabase.IFF_30min_delta ON aapl_30min_delta.AAPL_dateTime = IFF_dateTime \
     FULL JOIN deltabase.IGT_30min_delta ON aapl_30min_delta.AAPL_dateTime = IGT_dateTime \
     FULL JOIN deltabase.IHRT_30min_delta ON aapl_30min_delta.AAPL_dateTime = IHRT_dateTime \
     FULL JOIN deltabase.ILMN_30min_delta ON aapl_30min_delta.AAPL_dateTime = ILMN_dateTime \
     FULL JOIN deltabase.INCY_30min_delta ON aapl_30min_delta.AAPL_dateTime = INCY_dateTime \
     FULL JOIN deltabase.INFO_30min_delta ON aapl_30min_delta.AAPL_dateTime = INFO_dateTime \
     FULL JOIN deltabase.INFY_30min_delta ON aapl_30min_delta.AAPL_dateTime = INFY_dateTime \
     FULL JOIN deltabase.INTC_30min_delta ON aapl_30min_delta.AAPL_dateTime = INTC_dateTime \
     FULL JOIN deltabase.INTU_30min_delta ON aapl_30min_delta.AAPL_dateTime = INTU_dateTime \
     FULL JOIN deltabase.IP_30min_delta ON aapl_30min_delta.AAPL_dateTime = IP_dateTime \
     FULL JOIN deltabase.IPG_30min_delta ON aapl_30min_delta.AAPL_dateTime = IPG_dateTime \
     FULL JOIN deltabase.IPGP_30min_delta ON aapl_30min_delta.AAPL_dateTime = IPGP_dateTime \
     FULL JOIN deltabase.IQV_30min_delta ON aapl_30min_delta.AAPL_dateTime = IQV_dateTime \
     FULL JOIN deltabase.IR_30min_delta ON aapl_30min_delta.AAPL_dateTime = IR_dateTime \
     FULL JOIN deltabase.IRM_30min_delta ON aapl_30min_delta.AAPL_dateTime = IRM_dateTime \
     FULL JOIN deltabase.ISRG_30min_delta ON aapl_30min_delta.AAPL_dateTime = ISRG_dateTime \
     FULL JOIN deltabase.IT_30min_delta ON aapl_30min_delta.AAPL_dateTime = IT_dateTime \
     FULL JOIN deltabase.ITT_30min_delta ON aapl_30min_delta.AAPL_dateTime = ITT_dateTime \
     FULL JOIN deltabase.ITW_30min_delta ON aapl_30min_delta.AAPL_dateTime = ITW_dateTime \
     FULL JOIN deltabase.IVZ_30min_delta ON aapl_30min_delta.AAPL_dateTime = IVZ_dateTime \
     FULL JOIN deltabase.J_30min_delta ON aapl_30min_delta.AAPL_dateTime = J_dateTime \
     FULL JOIN deltabase.JBHT_30min_delta ON aapl_30min_delta.AAPL_dateTime = JBHT_dateTime \
     FULL JOIN deltabase.JBL_30min_delta ON aapl_30min_delta.AAPL_dateTime = JBL_dateTime \
     FULL JOIN deltabase.JCI_30min_delta ON aapl_30min_delta.AAPL_dateTime = JCI_dateTime \
     FULL JOIN deltabase.JD_30min_delta ON aapl_30min_delta.AAPL_dateTime = JD_dateTime \
     FULL JOIN deltabase.JEF_30min_delta ON aapl_30min_delta.AAPL_dateTime = JEF_dateTime \
     FULL JOIN deltabase.JKHY_30min_delta ON aapl_30min_delta.AAPL_dateTime = JKHY_dateTime \
     FULL JOIN deltabase.JNJ_30min_delta ON aapl_30min_delta.AAPL_dateTime = JNJ_dateTime \
     FULL JOIN deltabase.JNPR_30min_delta ON aapl_30min_delta.AAPL_dateTime = JNPR_dateTime \
     FULL JOIN deltabase.JP_30min_delta ON aapl_30min_delta.AAPL_dateTime = JP_dateTime \
     FULL JOIN deltabase.JPM_30min_delta ON aapl_30min_delta.AAPL_dateTime = JPM_dateTime \
     FULL JOIN deltabase.JWN_30min_delta ON aapl_30min_delta.AAPL_dateTime = JWN_dateTime \
     FULL JOIN deltabase.K_30min_delta ON aapl_30min_delta.AAPL_dateTime = K_dateTime \
     FULL JOIN deltabase.KBH_30min_delta ON aapl_30min_delta.AAPL_dateTime = KBH_dateTime \
     FULL JOIN deltabase.KEY_30min_delta ON aapl_30min_delta.AAPL_dateTime = KEY_dateTime \
     FULL JOIN deltabase.KEYS_30min_delta ON aapl_30min_delta.AAPL_dateTime = KEYS_dateTime \
     FULL JOIN deltabase.KHC_30min_delta ON aapl_30min_delta.AAPL_dateTime = KHC_dateTime \
     FULL JOIN deltabase.KIM_30min_delta ON aapl_30min_delta.AAPL_dateTime = KIM_dateTime \
     FULL JOIN deltabase.KLAC_30min_delta ON aapl_30min_delta.AAPL_dateTime = KLAC_dateTime \
     FULL JOIN deltabase.KMB_30min_delta ON aapl_30min_delta.AAPL_dateTime = KMB_dateTime \
     FULL JOIN deltabase.KMI_30min_delta ON aapl_30min_delta.AAPL_dateTime = KMI_dateTime \
     FULL JOIN deltabase.KMX_30min_delta ON aapl_30min_delta.AAPL_dateTime = KMX_dateTime \
     FULL JOIN deltabase.KO_30min_delta ON aapl_30min_delta.AAPL_dateTime = KO_dateTime \
     FULL JOIN deltabase.KODK_30min_delta ON aapl_30min_delta.AAPL_dateTime = KODK_dateTime \
     FULL JOIN deltabase.KR_30min_delta ON aapl_30min_delta.AAPL_dateTime = KR_dateTime \
     FULL JOIN deltabase.KSS_30min_delta ON aapl_30min_delta.AAPL_dateTime = KSS_dateTime \
     FULL JOIN deltabase.KSU_30min_delta ON aapl_30min_delta.AAPL_dateTime = KSU_dateTime \
     FULL JOIN deltabase.L_30min_delta ON aapl_30min_delta.AAPL_dateTime = L_dateTime \
     FULL JOIN deltabase.LBTYK_30min_delta ON aapl_30min_delta.AAPL_dateTime = AAL_dateTime \
     FULL JOIN deltabase.LDOS_30min_delta ON aapl_30min_delta.AAPL_dateTime = AAP_dateTime \
     FULL JOIN deltabase.LEG_30min_delta ON aapl_30min_delta.AAPL_dateTime = A_dateTime \
     FULL JOIN deltabase.LEN_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABBV_dateTime \
     FULL JOIN deltabase.LH_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABC_dateTime \
     FULL JOIN deltabase.LHX_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABMD_dateTime \
     FULL JOIN deltabase.LIFE_30min_delta ON aapl_30min_delta.AAPL_dateTime = ABT_dateTime \
     FULL JOIN deltabase.LIN_30min_delta ON aapl_30min_delta.AAPL_dateTime = ACN_dateTime \
     FULL JOIN deltabase.LKQ_30min_delta ON aapl_30min_delta.AAPL_dateTime = ACV_dateTime \
     FULL JOIN deltabase.LLY_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADBE_dateTime \
     FULL JOIN deltabase.LMT_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADI_dateTime \
     FULL JOIN deltabase.LNC_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADM_dateTime \
     FULL JOIN deltabase.LNT_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADP_dateTime \
     FULL JOIN deltabase.LOGI_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADS_dateTime \
     FULL JOIN deltabase.LOW_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADSK_dateTime \
     FULL JOIN deltabase.LRCX_30min_delta ON aapl_30min_delta.AAPL_dateTime = ADT_dateTime \
     FULL JOIN deltabase.LSI_30min_delta ON aapl_30min_delta.AAPL_dateTime = AEE_dateTime \
     FULL JOIN deltabase.LU_30min_delta ON aapl_30min_delta.AAPL_dateTime = AEP_dateTime \
     FULL JOIN deltabase.LUMN_30min_delta ON aapl_30min_delta.AAPL_dateTime = AES_dateTime \
     FULL JOIN deltabase.LUV_30min_delta ON aapl_30min_delta.AAPL_dateTime = AFL_dateTime \
     FULL JOIN deltabase.LVS_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIG_dateTime \
     FULL JOIN deltabase.LW_30min_delta ON aapl_30min_delta.AAPL_dateTime = AINV_dateTime \
     FULL JOIN deltabase.LYB_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIV_dateTime \
     FULL JOIN deltabase.LYV_30min_delta ON aapl_30min_delta.AAPL_dateTime = AIZ_dateTime \
     FULL JOIN deltabase.M_30min_delta ON aapl_30min_delta.AAPL_dateTime = AJG_dateTime \
     FULL JOIN deltabase.MA_30min_delta ON aapl_30min_delta.AAPL_dateTime = AKAM_dateTime \
     FULL JOIN deltabase.alb_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALB_dateTime \
     FULL JOIN deltabase.algn_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALGN_dateTime \
     FULL JOIN deltabase.alk_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALK_dateTime \
     FULL JOIN deltabase.all_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALL_dateTime \
     FULL JOIN deltabase.alle_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALLE_dateTime \
     FULL JOIN deltabase.altr_30min_delta ON aapl_30min_delta.AAPL_dateTime = ALTR_dateTime \
     FULL JOIN deltabase.amat_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMAT_dateTime \
     FULL JOIN deltabase.ambc_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMBC_dateTime \
     FULL JOIN deltabase.amcr_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMCR_dateTime \
     FULL JOIN deltabase.amd_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMD_dateTime \
     FULL JOIN deltabase.ame_30min_delta ON aapl_30min_delta.AAPL_dateTime = AME_dateTime \
     FULL JOIN deltabase.amg_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMG_dateTime \
     FULL JOIN deltabase.amgn_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMGN_dateTime \
     FULL JOIN deltabase.amp_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMP_dateTime \
     FULL JOIN deltabase.amt_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMT_dateTime \
     FULL JOIN deltabase.amzn_30min_delta ON aapl_30min_delta.AAPL_dateTime = AMZN_dateTime \
     FULL JOIN deltabase.an_30min_delta ON aapl_30min_delta.AAPL_dateTime = AN_dateTime \
     FULL JOIN deltabase.anet_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANET_dateTime \
     FULL JOIN deltabase.anf_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANF_dateTime \
     FULL JOIN deltabase.anss_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANSS_dateTime \
     FULL JOIN deltabase.antm_30min_delta ON aapl_30min_delta.AAPL_dateTime = ANTM_dateTime \
     FULL JOIN deltabase.aon_30min_delta ON aapl_30min_delta.AAPL_dateTime = AON_dateTime \
     FULL JOIN deltabase.aos_30min_delta ON aapl_30min_delta.AAPL_dateTime = AOS_dateTime \
     FULL JOIN deltabase.apa_30min_delta ON aapl_30min_delta.AAPL_dateTime = APA_dateTime \
     FULL JOIN deltabase.apd_30min_delta ON aapl_30min_delta.AAPL_dateTime = APD_dateTime \
     FULL JOIN deltabase.aph_30min_delta ON aapl_30min_delta.AAPL_dateTime = APH_dateTime \
     FULL JOIN deltabase.aptv_30min_delta ON aapl_30min_delta.AAPL_dateTime = APTV_dateTime \
     FULL JOIN deltabase.are_30min_delta ON aapl_30min_delta.AAPL_dateTime = ARE_dateTime \
     FULL JOIN deltabase.arnc_30min_delta ON aapl_30min_delta.AAPL_dateTime = ARNC_dateTime \
     FULL JOIN deltabase.ash_30min_delta ON aapl_30min_delta.AAPL_dateTime = ASH_dateTime \
     FULL JOIN deltabase.aso_30min_delta ON aapl_30min_delta.AAPL_dateTime = ASO_dateTime \
     FULL JOIN deltabase.atge_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATGE_dateTime \
     FULL JOIN deltabase.ati_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATI_dateTime \
     FULL JOIN deltabase.ato_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATO_dateTime \
     FULL JOIN deltabase.atvi_30min_delta ON aapl_30min_delta.AAPL_dateTime = ATVI_dateTime \
     FULL JOIN deltabase.avb_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVB_dateTime \
     FULL JOIN deltabase.avgo_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVGO_dateTime \
     FULL JOIN deltabase.avy_30min_delta ON aapl_30min_delta.AAPL_dateTime = AVY_dateTime \
     FULL JOIN deltabase.awk_30min_delta ON aapl_30min_delta.AAPL_dateTime = AWK_dateTime \
     FULL JOIN deltabase.axp_30min_delta ON aapl_30min_delta.AAPL_dateTime = AXP_dateTime \
     FULL JOIN deltabase.ayi_30min_delta ON aapl_30min_delta.AAPL_dateTime = AYI_dateTime \
     FULL JOIN deltabase.azo_30min_delta ON aapl_30min_delta.AAPL_dateTime = AZO_dateTime \
     ORDER BY aapl_30min_delta.AAPL_dateTime ASC;
")

display(data)

# COMMAND ----------

spark.conf.set("spark.sql.execution.arrow.enabled", "true")

#https://cumsum.wordpress.com/2021/03/05/pandas-attributeerror-function-object-has-no-attribute-xxx/
data_pd = data.na.fill(0).pandas_api()

display(data_pd)

# COMMAND ----------

#Replaces the NULL values with a specified value 0.
data_pd_pct = data_pd.pct_change().fillna(0)

display(data_pd_pct)

# COMMAND ----------

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

train_data = scaler.fit(data_pd_pct)

# COMMAND ----------

# initial cluster count
initial_n = 4
 
# train the model
initial_model = KMeans(n_clusters=initial_n)
 
# fit and predict per-household cluster assignment
init_clusters = initial_model.fit_predict(train_data)

# COMMAND ----------

score = metrics.silhouette_score(X, y_cluster_kmeans)
score

# COMMAND ----------

wcss.append(kmeans.inertia_)