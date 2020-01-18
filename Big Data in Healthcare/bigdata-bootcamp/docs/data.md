---
layout: SpecialPage
---
# Data

[[toc]]

## MIMIC-III

For both homework and project, we will use [MIMIC-III Critical Care Database](https://mimic.mit.edu/about/mimic/). This page describes information about the dataset and procedures to obtain the dataset.

### About MIMIC-III

[MIMIC-III](https://mimic.mit.edu/about/mimic/) is a large, openly-available database comprising deidentified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.

Among the types of data included are:

1. General - Patient demographics, hospital admissions & discharge dates, room tracking, death dates (in or out of the hospital), ICD-9 codes, unique code for health care provider and type (RN, MD, RT, etc). All dates are surrogate dates because of privacy issues, but time intervals (even those between multiple admissions of the same patient) are preserved.
2. Physiological - Hourly vital sign metrics, SAPS, SOFA, ventilator settings, etc.
3. Medications - IV meds, provider order entry data, etc.
4. Lab Tests - Chemistry, hematology, ABGs, imaging, etc.
5. Fluid Balance - Intake (solutions, blood, etc) and output (urine, estimated blood loss, etc).
6. Notes & Reports - Discharge summary, nursing progress notes, etc; cardiac catheterization, ECG, radiology, and echo reports.

MIMIC supports a diverse range of analytic studies spanning epidemiology, clinical decision-rule improvement, and electronic tool development. It is notable for three factors:

1. it is publicly and freely available
2. it encompasses a diverse and very large population of ICU patients
3. it contains high temporal resolution data including lab results, electronic documentation, and bedside monitor trends and waveforms.

### Request MIMIC Access

During this course, we will be working with the MIMIC database. MIMIC, although de-identified, still contains detailed information regarding the clinical care of patients, and must be treated with appropriate care and respect.

**You must finish CITI training first to get MIMIC access.**   **Do NOT request access individually.**

We will collect all student information and send a batch request to MIT, after which you'll be notified and send the access request.


<NotInUse>

In order to obtain access, it is necessary to:

1. Create a PhysioNet account.
    - Follow instructions here: [https://physionet.org/pnw/login](https://physionet.org/pnw/login)
    - For most, enter email and select "Create account"

2. Request MIMIC access.
    - Login using your account to [request access](https://physionet.org/works/MIMICIIIClinicalDatabase/access.shtml)
    - Review the data use agreement and select "I agree"
    - Fill the form and upload all your certifications. Some informaiton you may need

        - Reference category: **Supervisor**
        - Reference's name: **Jimeng Sun**
        - Reference's telephone number: **404.894.0482**
        - Reference's email address: **jsun@cc.gatech.edu**
        - Reference's title: **PI**
        - General research area for which the data will be used: **CSE8803 Big Data Analytics for Healthcare, Fall 2016**
    - Submit the form

</NotInUse>

## Bootcamp Training Material

Throughout the training exercises on this site we will use a small sample data set. If you followed the instructions documented on the [environment setup](/env/) page to set up your environment, you will find the sample data in the `/bigdata-bootcamp/data` folder in the virtual environment.

There are two data files with names `case.csv` and `control.csv` respectively. For the purpose of these exercises we will define patients who developed heart failure (HF) at some time point as case patients, and those who didn't develop HF as control patients.

Each line of the sample data file consists of a tuple structured as `(patient-id, event-id, timestamp, value)`, below are a few lines as an example:

```
020E860BD31CAC69,DRUG36987254604,968,30.0
020E860BD31CAC69,DRUG64158080642,974,30.0
020E860BD31CAC69,DRUG00440128228,976,60.0
020E860BD31CAC69,DIAG486,907,1.0
020E860BD31CAC69,DIAG7863,907,1.0
020E860BD31CAC69,DIAGV5866,907,1.0
020E860BD31CAC69,DIAG3659,907,1.0
020E860BD31CAC69,DIAGRG199,907,1.0
020E860BD31CAC69,PAYMENT,907,15000.0
020E860BD31CAC69,heartfailure,956,1.0
```

- `patient-id` is just a patient identifier (id) in order to differentiate records from different patients. For example, the portion of data we show above is all about the same patient, who has an id of `020E860BD31CAC69`.
- `event-id` encodes all the clinical events that a patient has had. For example, `DRUG00440128228` indicates that the patient was taking a drug identified by a National Drug Code of `00440128228`. The numbers in `DIAG486` are the first 3 digits of an [ICD9 code](https://www.cms.gov/medicare-coverage-database/staticpages/icd-9-code-lookup.aspx), which in this case is the code for [Pneumonia](http://www.icd9data.com/2012/Volume1/460-519/480-488/486/486.htm). For this data an event-id of `PAYMENT` means that the patient made a payment with the corresponding dollar amount.
- `timestamp` indicates the date at which the event on that row happened. Here the timestamp is not formatted as a real date but rather as an offset from an unspecified start point. This is done both to improve the simplicity of processing and to protect the privacy of the patients' data.
- `value` is the associated value for an event. See the below table for a detailed description data in the value field.

|event type| sample `event-od`| value meaning| example|
|---------:|:-----------------|:-------------|:-------------|
|diagnostic code|DIAG486|Will always be `1.0` for diagnose events| 1.0 |
|drug consumption|DRUG00440128228|Dosage of the drug|30|
|payment|PAYMENT|Amount of payment made on `timestamp` date| 15000|
|heartfailure|heartfailure|Indicator of heart failure event| 1.0 |

<NotInUse>

For `drug` the value corresponds to the drug dosage, for `payment` the value corresponds to the dollar amount of the payment, and for `diagnostic` events like `DIAG486` the value will always be `1` (which simply means the event happened and can be useful for counting events). The event `heartfailure` is a little bit different. You will find that the event `heartfailure` has `value` of `0` for control patients, and a `value` of `1` for case patients. The above sample data shows that patient `020E860BD31CAC69` was diagnosed with heart failure at timestamp 956.

</NotInUse>
