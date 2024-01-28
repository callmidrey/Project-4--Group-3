-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Buraeu" (
    "SK_ID_CURR" int   NOT NULL,
    "SK_ID_BUREAU" int   NOT NULL,
    "CREDIT_ACTIVE" varchar   NOT NULL,
    "CREDIT_CURRENCY" varchar   NOT NULL,
    "DAYS_CREDIT" int   NOT NULL,
    "CREDIT_DAY_OVERDUE" int   NOT NULL,
    "DAYS_CREDIT_ENDDATE" int   NOT NULL,
    "DAYS_ENDDATE_FACT" int   NOT NULL,
    "AMT_CREDIT_MAX_OVERDUE" int   NOT NULL,
    "CNT_CREDIT_PROLONG" int   NOT NULL,
    "AMT_CREDIT_SUM" int   NOT NULL,
    "AMT_CREDIT_SUM_DEBT" int   NOT NULL,
    "AMT_CREDIT_SUM_LIMIT" int   NOT NULL,
    "AMT_CREDIT_SUM_OVERDUE" int   NOT NULL,
    "CREDIT_TYPE" varchar   NOT NULL,
    "DAYS_CREDIT_UPDATE" int   NOT NULL,
    "AMT_ANNUITY" int   NOT NULL,
    CONSTRAINT "pk_Buraeu" PRIMARY KEY (
        "SK_ID_CURR","SK_ID_BUREAU"
     )
);

CREATE TABLE "Bureau_balance" (
    "SK_ID_BUREAU" int   NOT NULL,
    "MONTHS_BALANCE" int   NOT NULL,
    "STATUS" varchar   NOT NULL
);

CREATE TABLE "credit_card_balance" (
    "SK_ID_PREV" int   NOT NULL,
    "SK_ID_CURR" int   NOT NULL,
    "MONTHS_BALANCE" int   NOT NULL,
    "AMT_BALANCE" int   NOT NULL,
    "AMT_CREDIT_LIMIT_ACTUAL" int   NOT NULL,
    "AMT_DRAWINGS_ATM_CURRENT" int   NOT NULL,
    "AMT_DRAWINGS_CURRENT" int   NOT NULL,
    "AMT_DRAWINGS_OTHER_CURRENT" int   NOT NULL,
    "AMT_DRAWINGS_POS_CURRENT" int   NOT NULL,
    "AMT_INST_MIN_REGULARITY" int   NOT NULL,
    "AMT_PAYMENT_CURRENT" int   NOT NULL,
    "AMT_PAYMENT_TOTAL_CURRENT" int   NOT NULL,
    "AMT_RECEIVABLE_PRINCIPAL" int   NOT NULL,
    "AMT_RECIVABLE" int   NOT NULL,
    "AMT_TOTAL_RECEIVABLE" int   NOT NULL,
    "CNT_DRAWINGS_ATM_CURRENT" int   NOT NULL,
    "CNT_DRAWINGS_CURRENT" int   NOT NULL,
    "CNT_DRAWINGS_OTHER_CURRENT" int   NOT NULL,
    "CNT_DRAWINGS_POS_CURRENT" int   NOT NULL,
    "CNT_INSTALMENT_MATURE_CUM" int   NOT NULL,
    "NAME_CONTRACT_STATUS" varchar   NOT NULL,
    "SK_DPD" int   NOT NULL,
    "SK_DPD_DEF" int   NOT NULL,
    CONSTRAINT "pk_credit_card_balance" PRIMARY KEY (
        "SK_ID_PREV"
     )
);

CREATE TABLE "installments_payments" (
    "SK_ID_PREV" int   NOT NULL,
    "SK_ID_CURR" int   NOT NULL,
    "NUM_INSTALMENT_VERSION" int   NOT NULL,
    "NUM_INSTALMENT_NUMBER" int   NOT NULL,
    "DAYS_INSTALMENT" int   NOT NULL,
    "DAYS_ENTRY_PAYMENT" int   NOT NULL,
    "AMT_INSTALMENT" int   NOT NULL,
    "AMT_PAYMENT" int   NOT NULL
);

CREATE TABLE "POS_CASH_balance" (
    "SK_ID_PREV" int   NOT NULL,
    "SK_ID_CURR" int   NOT NULL,
    "MONTHS_BALANCE" int   NOT NULL,
    "CNT_INSTALMENT" int   NOT NULL,
    "CNT_INSTALMENT_FUTURE" int   NOT NULL,
    "NAME_CONTRACT_STATUS" varchar   NOT NULL,
    "SK_DPD" int   NOT NULL,
    "SK_DPD_DEF" int   NOT NULL
);

ALTER TABLE "Buraeu" ADD CONSTRAINT "fk_Buraeu_SK_ID_CURR" FOREIGN KEY("SK_ID_CURR")
REFERENCES "credit_card_balance" ("SK_ID_CURR");

ALTER TABLE "Buraeu" ADD CONSTRAINT "fk_Buraeu_SK_ID_BUREAU" FOREIGN KEY("SK_ID_BUREAU")
REFERENCES "Bureau_balance" ("SK_ID_BUREAU");

ALTER TABLE "credit_card_balance" ADD CONSTRAINT "fk_credit_card_balance_SK_ID_PREV_SK_ID_CURR" FOREIGN KEY("SK_ID_PREV", "SK_ID_CURR")
REFERENCES "installments_payments" ("SK_ID_PREV", "SK_ID_CURR");

ALTER TABLE "installments_payments" ADD CONSTRAINT "fk_installments_payments_SK_ID_PREV_SK_ID_CURR" FOREIGN KEY("SK_ID_PREV", "SK_ID_CURR")
REFERENCES "POS_CASH_balance" ("SK_ID_PREV", "SK_ID_CURR");

