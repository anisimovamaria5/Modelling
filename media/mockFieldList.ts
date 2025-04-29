export interface Company {
    id: number;
    companyName: string;
    code: string;
    fieldList: Field[];
}

export interface Field {
    id: number;
    fieldName: string;
    code: string;
    dksList: DKS[];
}

export interface DKS {
    id: number;
    dksName: string;
    code: string;
    spchList: SPCH[];
}

export interface SPCH {
    id: number;
    spchName: string;
    code: string;
}

export const companies: Company[] = [
    {
        id: 1,
        companyName: "Газпром добыча Ноябрьск",
        code: "GDN",
        fieldList: [
            {
                id: 1,
                fieldName: "Вынгаяхинское",
                code: "GDN_VNG",
                dksList: [
                    {
                        id: 1,
                        dksName: "ДКС",
                        code: "GDN_VNG_DKS1",
                        spchList: [
                            { id: 1, spchName: "СПЧ 21-2,2", code: "GDN_VNG_DKS1_SPCH21-2.2" },
                            { id: 2, spchName: "СПЧ 41-2,2", code: "GDN_VNG_DKS1_SPCH41-2.2" },
                            { id: 3, spchName: "СПЧ 76-2,2", code: "GDN_VNG_DKS1_SPCH76-2.2" }
                        ]
                    }
                ]
            },
            {
                id: 2,
                fieldName: "Еты-Пуровское",
                code: "GDN_ETP",
                dksList: [
                    {
                        id: 2,
                        dksName: "ДКС",
                        code: "GDN_ETP_DKS1",
                        spchList: [
                            { id: 4, spchName: "СПЧ 21-2,2", code: "GDN_ETP_DKS1_SPCH21-2.2" }
                        ]
                    }
                ]
            },
            {
                id: 3,
                fieldName: "Западно-Таркосалинское",
                code: "GDN_ZTS",
                dksList: [
                    {
                        id: 3,
                        dksName: "ДКС",
                        code: "GDN_ZTS_DKS1",
                        spchList: [
                            { id: 5, spchName: "СПЧ 21-3,0", code: "GDN_ZTS_DKS1_SPCH21-3.0" },
                            { id: 6, spchName: "СПЧ 41-2,2", code: "GDN_ZTS_DKS1_SPCH41-2.2" },
                            { id: 7, spchName: "СПЧ 76-2,2", code: "GDN_ZTS_DKS1_SPCH76-2.2" }
                        ]
                    }
                ]
            },
            {
                id: 4,
                fieldName: "Комсомольское",
                code: "GDN_KMS",
                dksList: [
                    {
                        id: 4,
                        dksName: "ДКС",
                        code: "GDN_KMS_DKS1",
                        spchList: [
                            { id: 8, spchName: "СПЧ 21-3,0", code: "GDN_KMS_DKS1_SPCH21-3.0" },
                            { id: 9, spchName: "СПЧ 21-3,0 УЛХ 3,1", code: "GDN_KMS_DKS1_SPCH21-3.0-ULH3.1" },
                            { id: 10, spchName: "СПЧ 45-3,0", code: "GDN_KMS_DKS1_SPCH45-3.0" },
                            { id: 11, spchName: "СПЧ 76-2,2", code: "GDN_KMS_DKS1_SPCH76-2.2" },
                            { id: 12, spchName: "СПЧ 76-1,7", code: "GDN_KMS_DKS1_SPCH76-1.7" }
                        ]
                    }
                ]
            },
            {
                id: 5,
                fieldName: "Губкинское",
                code: "GDN_GBK",
                dksList: [
                    {
                        id: 5,
                        dksName: "ДКС",
                        code: "GDN_GBK_DKS1",
                        spchList: [
                            { id: 13, spchName: "СПЧ-294ГЦ2-825/9,5-21", code: "GDN_GBK_DKS1_SPCH294GC2-825-9.5-21" },
                            { id: 14, spchName: "СПЧ 16-41/2,2", code: "GDN_GBK_DKS1_SPCH16-41-2.2" },
                            { id: 15, spchName: "СПЧ-295ГЦ2-440/18,5-41", code: "GDN_GBK_DKS1_SPCH295GC2-440-18.5-41" },
                            { id: 16, spchName: "СПЧ-295ГЦ2-195/25-76", code: "GDN_GBK_DKS1_SPCH295GC2-195-25-76" },
                            { id: 17, spchName: "СПЧ-Ц-16С/76-3,0", code: "GDN_GBK_DKS1_SPCH-C-16S-76-3.0" }
                        ]
                    }
                ]
            }
        ]
    },
    {
        id: 2,
        companyName: "Газпром добыча Надым",
        code: "GDM",
        fieldList: [
            {
                id: 6,
                fieldName: "Бованенковское",
                code: "GDM_BOV",
                dksList: [
                    {
                        id: 6,
                        dksName: "ДКС1 ГП1",
                        code: "GDM_BOV_DKS1-GP1",
                        spchList: [
                            { id: 18, spchName: "НЦ-25 ДКС", code: "GDM_BOV_DKS1-GP1_NC25" }
                        ]
                    },
                    {
                        id: 7,
                        dksName: "ДКС2 ГП1",
                        code: "GDM_BOV_DKS2-GP1",
                        spchList: [
                            { id: 19, spchName: "СПЧ-488-16/120-1,7", code: "GDM_BOV_DKS2-GP1_SPCH488-16-120-1.7" }
                        ]
                    },
                    {
                        id: 8,
                        dksName: "ДКС3 ГП1",
                        code: "GDM_BOV_DKS3-GP1",
                        spchList: [
                            { id: 20, spchName: "СПЧ 285-16/70-1,8-С", code: "GDM_BOV_DKS3-GP1_SPCH285-16-70-1.8-S" }
                        ]
                    },
                    {
                        id: 9,
                        dksName: "ДКС1 ГП2.1",
                        code: "GDM_BOV_DKS1-GP2.1",
                        spchList: [
                            { id: 21, spchName: "СПЧ-588-16/75-1,9", code: "GDM_BOV_DKS1-GP2.1_SPCH588-16-75-1.9" }
                        ]
                    },
                    {
                        id: 10,
                        dksName: "ДКС2 ГП2.1",
                        code: "GDM_BOV_DKS2-GP2.1",
                        spchList: [
                            { id: 22, spchName: "СПЧ-488-16/120-1,7", code: "GDM_BOV_DKS2-GP2.1_SPCH488-16-120-1.7" },
                            { id: 23, spchName: "СПЧ-285-16/121-1,7", code: "GDM_BOV_DKS2-GP2.1_SPCH285-16-121-1.7" }
                        ]
                    },
                    {
                        id: 11,
                        dksName: "ДКС3 ГП2.1",
                        code: "GDM_BOV_DKS3-GP2.1",
                        spchList: [
                            { id: 24, spchName: "СПЧ 285-16/70-1,8-С", code: "GDM_BOV_DKS3-GP2.1_SPCH285-16-70-1.8-S" }
                        ]
                    },
                    {
                        id: 12,
                        dksName: "ДКС1 ГП2.2",
                        code: "GDM_BOV_DKS1-GP2.2",
                        spchList: [
                            { id: 25, spchName: "НЦ-25 ДКС", code: "GDM_BOV_DKS1-GP2.2_NC25" }
                        ]
                    },
                    {
                        id: 13,
                        dksName: "ДКС2 ГП2.2",
                        code: "GDM_BOV_DKS2-GP2.2",
                        spchList: [
                            { id: 26, spchName: "СПЧ-488-16/120-1,7", code: "GDM_BOV_DKS2-GP2.2_SPCH488-16-120-1.7" },
                            { id: 27, spchName: "СПЧ-285-16/121-1,7", code: "GDM_BOV_DKS2-GP2.2_SPCH285-16-121-1.7" }
                        ]
                    },
                    {
                        id: 14,
                        dksName: "ДКС3 ГП-22",
                        code: "GDM_BOV_DKS3-GP2.2",
                        spchList: [
                            { id: 28, spchName: "СПЧ 285-16/70-1,8-С", code: "GDM_BOV_DKS3-GP2.2_SPCH285-16-70-1.8-S" }
                        ]
                    },
                    {
                        id: 15,
                        dksName: "ДКС1 ГП3",
                        code: "GDM_BOV_DKS1-GP3",
                        spchList: [
                            { id: 29, spchName: "НЦ-25 ДКС", code: "GDM_BOV_DKS1-GP3_NC25" }
                        ]
                    },
                    {
                        id: 16,
                        dksName: "ДКС2 ГП3",
                        code: "GDM_BOV_DKS2-GP3",
                        spchList: [
                            { id: 30, spchName: "СПЧ-285-16-121-2,2С", code: "GDM_BOV_DKS2-GP3_SPCH285-16-121-2.2S" }
                        ]
                    }
                ]
            },
            {
                id: 7,
                fieldName: "Медвежье",
                code: "GDM_MDV",
                dksList: [
                    {
                        id: 17,
                        dksName: "ДКС1",
                        code: "GDM_MDV_DKS1",
                        spchList: [
                            { id: 31, spchName: "ЦБК НЦ-6ДКС-02 \"Урал\" (СПЧ 2151-61-1С)", code: "GDM_MDV_DKS1_CBK-NC6-URAL-SPCH2151-61-1S" }
                        ]
                    },
                    {
                        id: 18,
                        dksName: "ДКС3",
                        code: "GDM_MDV_DKS3",
                        spchList: [
                            { id: 32, spchName: "ЦБК НЦ-6ДКС-02 \"Урал\" (СПЧ 6-20-3)", code: "GDM_MDV_DKS3_CBK-NC6-URAL-SPCH6-20-3" }
                        ]
                    },
                    {
                        id: 19,
                        dksName: "ДКС4",
                        code: "GDM_MDV_DKS4",
                        spchList: [
                            { id: 33, spchName: "НЦ-6ДКС-02 \"Урал\" (СПЧ 2151-61-1С)", code: "GDM_MDV_DKS4_NC6-URAL-SPCH2151-61-1S" }
                        ]
                    },
                    {
                        id: 20,
                        dksName: "ДКС6",
                        code: "GDM_MDV_DKS6",
                        spchList: [
                            { id: 34, spchName: "ЦБК 294ГЦ2-410/10-20М1235 (СПЧ-294-08/20-3,2-С)", code: "GDM_MDV_DKS6_CBK294GC2-410-10-20M1235-SPCH294-08-20-3.2-S" }
                        ]
                    },
                    {
                        id: 21,
                        dksName: "ДКС8",
                        code: "GDM_MDV_DKS8",
                        spchList: [
                            { id: 35, spchName: "Н-6-56 (КМЧ Н-6-20-1,95)", code: "GDM_MDV_DKS8_N6-56-KMCH-N6-20-1.95" }
                        ]
                    },
                    {
                        id: 22,
                        dksName: "ДКС9",
                        code: "GDM_MDV_DKS9",
                        spchList: [
                            { id: 36, spchName: "ЦБК 294ГЦ2-450/5-20М125 (16/20-4,0 (СНПО))", code: "GDM_MDV_DKS9_CBK294GC2-450-5-20M125-16-20-4.0-SNPO" }
                        ]
                    },
                    {
                        id: 23,
                        dksName: "ЦДКС",
                        code: "GDM_MDV_CDKS",
                        spchList: [
                            { id: 37, spchName: "СПЧ 16/28-1,6", code: "GDM_MDV_CDKS_SPCH16-28-1.6" },
                            { id: 38, spchName: "СПЧ 16/45-1,8", code: "GDM_MDV_CDKS_SPCH16-45-1.8" },
                            { id: 39, spchName: "НЦ 18/70-1,64", code: "GDM_MDV_CDKS_NC18-70-1.64" }
                        ]
                    }
                ]
            },
            {
                id: 8,
                fieldName: "Юбилейное",
                code: "GDM_YUB",
                dksList: [
                    {
                        id: 24,
                        dksName: "ДКС",
                        code: "GDM_YUB_DKS1",
                        spchList: [
                            { id: 40, spchName: "СПЧ 498-3,0/21-16", code: "GDM_YUB_DKS1_SPCH498-3.0-21-16" },
                            { id: 41, spchName: "СПЧ 498-2,2/30-16", code: "GDM_YUB_DKS1_SPCH498-2.2-30-16" },
                            { id: 42, spchName: "СПЧ 498-3,0/76-16", code: "GDM_YUB_DKS1_SPCH498-3.0-76-16" }
                        ]
                    }
                ]
            },
            {
                id: 9,
                fieldName: "Ямсовейское",
                code: "GDM_YMS",
                dksList: [
                    {
                        id: 25,
                        dksName: "ДКС",
                        code: "GDM_YMS_DKS1",
                        spchList: [
                            { id: 43, spchName: "СПЧ 498-3,0/30-16", code: "GDM_YMS_DKS1_SPCH498-3.0-30-16" },
                            { id: 44, spchName: "СПЧ 498-3,0/76-16", code: "GDM_YMS_DKS1_SPCH498-3.0-76-16" }
                        ]
                    }
                ]
            }
        ]
    },
    {
        id: 3,
        companyName: "Газпром добыча Уренгой",
        code: "GDU",
        fieldList: [
            {
                id: 10,
                fieldName: "Уренгойское",
                code: "GDU_URG",
                dksList: [
                    {
                        id: 26,
                        dksName: "ДКС1",
                        code: "GDU_URG_DKS1",
                        spchList: [
                            { id: 45, spchName: "СПЧ 16-30-3.0МУ", code: "GDU_URG_DKS1_SPCH16-30-3.0MU" },
                            { id: 46, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS1_SPCH16-30-3.5MU" },
                            { id: 47, spchName: "СПЧ 16-76-2.0 М2", code: "GDU_URG_DKS1_SPCH16-76-2.0-M2" }
                        ]
                    },
                    {
                        id: 27,
                        dksName: "ДКС1А",
                        code: "GDU_URG_DKS1A",
                        spchList: [
                            { id: 48, spchName: "СПЧ-16/30-3,5 МУ", code: "GDU_URG_DKS1A_SPCH16-30-3.5-MU" },
                            { id: 49, spchName: "СПЧ 16/41-2.2", code: "GDU_URG_DKS1A_SPCH16-41-2.2" },
                            { id: 50, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS1A_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 28,
                        dksName: "ДКС2",
                        code: "GDU_URG_DKS2",
                        spchList: [
                            { id: 51, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS2_SPCH16-30-3.5MU" },
                            { id: 52, spchName: "СПЧ 16-76-2.0", code: "GDU_URG_DKS2_SPCH16-76-2.0" }
                        ]
                    },
                    {
                        id: 29,
                        dksName: "ДКС3",
                        code: "GDU_URG_DKS3",
                        spchList: [
                            { id: 53, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS3_SPCH16-30-3.5MU" },
                            { id: 54, spchName: "СПЧ 16-76-2.0МУ", code: "GDU_URG_DKS3_SPCH16-76-2.0MU" }
                        ]
                    },
                    {
                        id: 30,
                        dksName: "ДКС4",
                        code: "GDU_URG_DKS4",
                        spchList: [
                            { id: 55, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS4_SPCH16-30-3.5MU" },
                            { id: 56, spchName: "СПЧ 16-76-2.0МУ", code: "GDU_URG_DKS4_SPCH16-76-2.0MU" },
                            { id: 57, spchName: "СПЧ 16-76-2,0М", code: "GDU_URG_DKS4_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 31,
                        dksName: "ДКС5",
                        code: "GDU_URG_DKS5",
                        spchList: [
                            { id: 58, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS5_SPCH16-30-3.5MU" },
                            { id: 59, spchName: "СПЧ 16-76-2.0", code: "GDU_URG_DKS5_SPCH16-76-2.0" }
                        ]
                    },
                    {
                        id: 32,
                        dksName: "ДКС6",
                        code: "GDU_URG_DKS6",
                        spchList: [
                            { id: 60, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS6_SPCH16-30-3.5MU" },
                            { id: 61, spchName: "СПЧ 16-76-2.0 (СМ2)", code: "GDU_URG_DKS6_SPCH16-76-2.0-SM2" }
                        ]
                    },
                    {
                        id: 33,
                        dksName: "ДКС7",
                        code: "GDU_URG_DKS7",
                        spchList: [
                            { id: 62, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS7_SPCH16-30-3.5MU" },
                            { id: 63, spchName: "СПЧ 16-76-2.0 (СМ2)", code: "GDU_URG_DKS7_SPCH16-76-2.0-SM2" },
                            { id: 64, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS7_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 34,
                        dksName: "ДКС8",
                        code: "GDU_URG_DKS8",
                        spchList: [
                            { id: 65, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS8_SPCH16-30-3.5MU" },
                            { id: 66, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS8_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 35,
                        dksName: "ДКС9",
                        code: "GDU_URG_DKS9",
                        spchList: [
                            { id: 67, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS9_SPCH16-30-3.5MU" },
                            { id: 68, spchName: "СПЧ 16-76-2.0 (СМ2)", code: "GDU_URG_DKS9_SPCH16-76-2.0-SM2" }
                        ]
                    },
                    {
                        id: 36,
                        dksName: "ДКС10",
                        code: "GDU_URG_DKS10",
                        spchList: [
                            { id: 69, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS10_SPCH16-30-3.5MU" },
                            { id: 70, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS10_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 37,
                        dksName: "ДКС11",
                        code: "GDU_URG_DKS11",
                        spchList: [
                            { id: 71, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS11_SPCH16-30-3.5MU" },
                            { id: 72, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS11_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 38,
                        dksName: "ДКС12",
                        code: "GDU_URG_DKS12",
                        spchList: [
                            { id: 73, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS12_SPCH16-30-3.5MU" },
                            { id: 74, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS12_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 39,
                        dksName: "ДКС13",
                        code: "GDU_URG_DKS13",
                        spchList: [
                            { id: 75, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS13_SPCH16-30-3.5MU" },
                            { id: 76, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS13_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 40,
                        dksName: "ДКС15",
                        code: "GDU_URG_DKS15",
                        spchList: [
                            { id: 77, spchName: "СПЧ 16-30-3.5МУ", code: "GDU_URG_DKS15_SPCH16-30-3.5MU" },
                            { id: 78, spchName: "СПЧ 16-76-2.0М", code: "GDU_URG_DKS15_SPCH16-76-2.0M" }
                        ]
                    },
                    {
                        id: 41,
                        dksName: "ДКС16",
                        code: "GDU_URG_DKS16",
                        spchList: [
                            { id: 79, spchName: "СПЧ 18/80-1,5", code: "GDU_URG_DKS16_SPCH18-80-1.5" },
                            { id: 80, spchName: "СПЧ 18/57-1,5", code: "GDU_URG_DKS16_SPCH18-57-1.5" }
                        ]
                    },
                    {
                        id: 42,
                        dksName: "ДКС1 АВ",
                        code: "GDU_URG_DKS1-AV",
                        spchList: [
                            { id: 81, spchName: "СПЧ 10/51-2,1", code: "GDU_URG_DKS1-AV_SPCH10-51-2.1" },
                            { id: 82, spchName: "СПЧ 10/76-2,2С", code: "GDU_URG_DKS1-AV_SPCH10-76-2.2S" }
                        ]
                    },
                    {
                        id: 43,
                        dksName: "ДКС2В",
                        code: "GDU_URG_DKS2V",
                        spchList: [
                            { id: 83, spchName: "СПЧ 10-41-2,2", code: "GDU_URG_DKS2V_SPCH10-41-2.2" },
                            { id: 84, spchName: "СПЧ 108-86-3,5", code: "GDU_URG_DKS2V_SPCH108-86-3.5" }
                        ]
                    },
                    {
                        id: 44,
                        dksName: "ДКС5В",
                        code: "GDU_URG_DKS5V",
                        spchList: [
                            { id: 85, spchName: "СПЧ 10/30-3,0", code: "GDU_URG_DKS5V_SPCH10-30-3.0" },
                            { id: 86, spchName: "СПЧ 14510/76-3.0С", code: "GDU_URG_DKS5V_SPCH14510-76-3.0S" }
                        ]
                    },
                    {
                        id: 45,
                        dksName: "ДКС-8В",
                        code: "GDU_URG_DKS8V",
                        spchList: [
                            { id: 87, spchName: "СПЧ-10/41-2,2", code: "GDU_URG_DKS8V_SPCH10-41-2.2" },
                            { id: 88, spchName: "СПЧ-10/76-3.0С", code: "GDU_URG_DKS8V_SPCH10-76-3.0S" }
                        ]
                    }
                ]
            }
        ]
    },
    {
        id: 4,
        companyName: "Севернефтегазпром",
        code: "SNG",
        fieldList: [
            {
                id: 11,
                fieldName: "Южно-Русское",
                code: "SNG_YUR",
                dksList: [
                    {
                        id: 46,
                        dksName: "ДКС",
                        code: "SNG_YUR_DKS1",
                        spchList: [
                            { id: 89, spchName: "СПЧ 16/40-2,5", code: "SNG_YUR_DKS1_SPCH16-40-2.5" },
                            { id: 90, spchName: "СПЧ 16/76-2,2(01)", code: "SNG_YUR_DKS1_SPCH16-76-2.2-01" }
                        ]
                    }
                ]
            }
        ]
    },
    {
        id: 5,
        companyName: "Газпром добыча Ямбург",
        code: "GDYMB",
        fieldList: [
            {
                id: 12,
                fieldName: "Ямбургское",
                code: "GDYMB_YMB",
                dksList: [
                    {
                        id: 47,
                        dksName: "ДКС1",
                        code: "GDYMB_YMB_DKS1",
                        spchList: [
                            { id: 91, spchName: "СПЧ 16/21-3,0(5200)", code: "GDYMB_YMB_DKS1_SPCH16-21-3.0-5200" },
                            { id: 92, spchName: "СПЧ 16/60-3,0", code: "GDYMB_YMB_DKS1_SPCH16-60-3.0" }
                        ]
                    },
                    {
                        id: 48,
                        dksName: "ДКС2",
                        code: "GDYMB_YMB_DKS2",
                        spchList: [
                            { id: 93, spchName: "СПЧ 16/21-3,0(5035)", code: "GDYMB_YMB_DKS2_SPCH16-21-3.0-5035" },
                            { id: 94, spchName: "СПЧ 16/60-3,0", code: "GDYMB_YMB_DKS2_SPCH16-60-3.0" }
                        ]
                    },
                    {
                        id: 49,
                        dksName: "ДКС3",
                        code: "GDYMB_YMB_DKS3",
                        spchList: [
                            { id: 95, spchName: "СПЧ 16/21-3,0(5200)", code: "GDYMB_YMB_DKS3_SPCH16-21-3.0-5200" },
                            { id: 96, spchName: "СПЧ 16/60-3,0", code: "GDYMB_YMB_DKS3_SPCH16-60-3.0" }
                        ]
                    },
                    {
                        id: 50,
                        dksName: "ДКС4",
                        code: "GDYMB_YMB_DKS4",
                        spchList: [
                            { id: 97, spchName: "СПЧ 16/21-3,0(5200)", code: "GDYMB_YMB_DKS4_SPCH16-21-3.0-5200" },
                            { id: 98, spchName: "СПЧ 16/76-2,2", code: "GDYMB_YMB_DKS4_SPCH16-76-2.2" }
                        ]
                    },
                    {
                        id: 51,
                        dksName: "ДКС5",
                        code: "GDYMB_YMB_DKS5",
                        spchList: [
                            { id: 99, spchName: "СПЧ 16/21-3,0(5035)", code: "GDYMB_YMB_DKS5_SPCH16-21-3.0-5035" },
                            { id: 100, spchName: "СПЧ 16/60-3,0", code: "GDYMB_YMB_DKS5_SPCH16-60-3.0" }
                        ]
                    },
                    {
                        id: 52,
                        dksName: "ДКС6",
                        code: "GDYMB_YMB_DKS6",
                        spchList: [
                            { id: 101, spchName: "СПЧ 16/21-3,0(5200)", code: "GDYMB_YMB_DKS6_SPCH16-21-3.0-5200" },
                            { id: 102, spchName: "СПЧ 16/60-3,0", code: "GDYMB_YMB_DKS6_SPCH16-60-3.0" }
                        ]
                    },
                    {
                        id: 53,
                        dksName: "ДКС7",
                        code: "GDYMB_YMB_DKS7",
                        spchList: [
                            { id: 103, spchName: "СПЧ 16/21-3,0(5200)", code: "GDYMB_YMB_DKS7_SPCH16-21-3.0-5200" },
                            { id: 104, spchName: "СПЧ 16/76-2,2", code: "GDYMB_YMB_DKS7_SPCH16-76-2.2" }
                        ]
                    },
                    {
                        id: 54,
                        dksName: "ДКС-9",
                        code: "GDYMB_YMB_DKS9",
                        spchList: [
                            { id: 105, spchName: "СПЧ 16/84-2,2", code: "GDYMB_YMB_DKS9_SPCH16-84-2.2" }
                        ]
                    },
                    {
                        id: 55,
                        dksName: "ДКС1В",
                        code: "GDYMB_YMB_DKS1V",
                        spchList: [
                            { id: 106, spchName: "СПЧ 7ГЦ2-573/7,2-40", code: "GDYMB_YMB_DKS1V_SPCH7GC2-573-7.2-40" },
                            { id: 107, spchName: "СПЧ 16/100-2,2(ККМ)", code: "GDYMB_YMB_DKS1V_SPCH16-100-2.2-KKM" }
                        ]
                    }
                ]
            },
            {
                id: 13,
                fieldName: "Заполярное",
                code: "GDYMB_ZPL",
                dksList: [
                    {
                        id: 56,
                        dksName: "ДКС1С",
                        code: "GDYMB_ZPL_DKS1S",
                        spchList: [
                            { id: 108, spchName: "СПЧ-425-16/65-1,7СМП", code: "GDYMB_ZPL_DKS1S_SPCH425-16-65-1.7SMP" }
                        ]
                    },
                    {
                        id: 57,
                        dksName: "ДКС2С",
                        code: "GDYMB_ZPL_DKS2S",
                        spchList: [
                            { id: 109, spchName: "СПЧ-425-16/65-1,7СМП", code: "GDYMB_ZPL_DKS2S_SPCH425-16-65-1.7SMP" }
                        ]
                    },
                    {
                        id: 58,
                        dksName: "ДКС3С",
                        code: "GDYMB_ZPL_DKS3S",
                        spchList: [
                            { id: 110, spchName: "СПЧ-425-16/65-1,7СМП", code: "GDYMB_ZPL_DKS3S_SPCH425-16-65-1.7SMP" }
                        ]
                    },
                    {
                        id: 581,
                        dksName: "ДКС1В",
                        code: "GDYMB_ZPL_DKS1V",
                        spchList: [
                            { id: 110, spchName: "СПЧ-425-16/65-1,7СМП", code: "GDYMB_ZPL_DKS1V_SPCH425-16-65-1.7SMP" }
                        ]
                    },
                    {
                        id: 582,
                        dksName: "ДКС2В",
                        code: "GDYMB_ZPL_DKS2V",
                        spchList: [
                            { id: 110, spchName: "СПЧ-425-16/65-1,7СМП", code: "GDYMB_ZPL_DKS2V_SPCH425-16-65-1.7SMP" }
                        ]
                    }
                ]
            }
        ]
    },
    {
        id: 6,
        companyName: "Газпром добыча Оренбург",
        code: "GDO",
        fieldList: [
            {
                id: 14,
                fieldName: "Оренбургское",
                code: "GDO_ORB",
                dksList: [
                    {
                        id: 59,
                        dksName: "ДКС",
                        code: "GDO_ORB_DKS1",
                        spchList: [
                            { id: 111, spchName: "ЭГПА-Ц-6,3/32К-2,2", code: "GDO_ORB_DKS1_EGPA-C-6.3-32K-2.2" },
                            { id: 112, spchName: "ЭГПА-Ц-6,3/67К-2,2", code: "GDO_ORB_DKS1_EGPA-C-6.3-67K-2.2" }
                        ]
                    }
                ]
            }
        ]
    }
];