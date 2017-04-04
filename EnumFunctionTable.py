from enum import Enum

class EnumFunctionTable(Enum):
    Adj_PHS = 1
    Adj_RSA = 2
    Adj_FAD = 3
    Adj_GET = 4
    Adj_ZAD = 5
    Tbg_DefChan = 6
    Adj_FAL = 7
    Adj_GAD = 8
    Adj_DSC = 9
    Tbg_AirCal = 10
    Tbg_ChanCorr = 11
    Tbg_Spacing = 12
    Tbg_WaterBeamHardCorrection = 13
    Tbg_WaterScaling = 14
    Qua_Slice_IEC = 15
    Qua_Slice_ConstRef = 16
    Qua_Contrast_IEC = 17
    Qua_Contrast_ConstRef = 18
    Qua_Noise_ConstRef = 19
    Qua_Homogeneity_ConstRef = 20
    Qua_MTF_IEC = 21
    Qua_MTF_ConstRef = 22
    Qua_TubeVoltage_ConstRef = 23
    Qua_TubeVoltage_IEC = 24
    Qua_TubePowerLevel_DHHS = 25
    Qua_TubePowerLevel_IEC = 26
    Qua_ScanDuration_DHHS = 27
    Tbg_AirCal_BascalOnly = 28
    Qua_Homogeneity_IEC = 29
    Qua_Noise_IEC = 30
    QuaSlice = 31
    QuaHomogeneity = 32
    QuaNoise = 33
    QuaMTF = 34
    QuaContrast = 35
    Qua_SagCorLightmarker_IEC = 36
    Qua_SagCorLightmarker_ConstRef = 37
    Qua_Lightmarker_IEC = 38
    Qua_TopoPos_IEC = 39
    Qua_TablePos_IEC = 40
    Qua_Lightmarker_ConstRef = 41
    Qua_TopoPos_ConstRef = 42
    Qua_TablePos_ConstRef = 43
    Qua_LowContrast_IEC = 44
    Qua_LowContrast_ConstRef = 45
    Qua_CTDIDose_IEC = 46
    Qua_TopoDose_IEC = 47
    Qua_CTDIDose_ConstRef = 48
    Qua_BeamQuality_DHHS = 49
    Qua_IECCTDIHEADID_IEC = 50
    Qua_IECCTDIHEADID_ConstRef = 51
    Qua_CTDIHEADID_DHHS = 52
    QuaIECCTDIBODYID = 53
    Qua_IECCTDIBODYID_IEC = 54
    Qua_IECCTDIBODYID_ConstRef = 55
    Qua_CTDIBODYID_DHHS = 56
    Qua_DoseProfile_IEC = 57
    Adj_FAD_Check = 58
    Tbg_AirCal_CusCalib_BascalOnly = 59
##############################################

if __name__ == '__main__':
    print(EnumFunctionTable(1))
