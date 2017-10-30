# HootMentor

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [HootMentor](#hootmentor)
	- [Getting Started](#getting-started)
		- [Prerequisites](#prerequisites)
		- [Installing](#installing)
	- [Deployment](#deployment)
	- [Authors](#authors)
	- [License](#license)
	- [Documentation](#documentation)
		- [API Access](#api-access)
			- [```/_ah/api/jobSearch/v1/jobSearch/echo```](#ahapijobsearchv1jobsearchecho)
			- [```/_ah/api/jobSearch/v1/jobSearch/findSimilar```](#ahapijobsearchv1jobsearchfindsimilar)
			- [```/_ah/api/jobSearch/v1/jobSearch/marketReportDetails```](#ahapijobsearchv1jobsearchmarketreportdetails)

<!-- /TOC -->

## Getting Started

### Prerequisites
- git
-

### Installing

## Deployment

## Authors

## License

## Documentation

### API Access

#### ```/_ah/api/jobSearch/v1/jobSearch/echo```

Echoes back given content for testing

Requires
```
{
  'content': 'string'
}
```

Returns
```
{
  'content': 'same string as above'
}
```

#### ```/_ah/api/jobSearch/v1/jobSearch/findSimilar```
Returns similar jobs based on the job title

(may be slow with initial requests...)

Requires
```
{
  'content': 'job name'
}
```
Returns
```
{
  'content': ['list', 'of', 'similar', 'job', 'titles']
}
```

- Example CURL request
  - Request
  ```
  curl -H "Content-Type: application/json" -X POST -d '{"content":"cashier"}' localhost:8080/_ah/api/jobSearch/
  ```

  - Response (may be changed)
  ```
  {
     "content": "[u'1114', u'1434', u'1312', u'6231', u'6231', u'6231', u'1314', u'1312']"
    }
  ```

#### ```/_ah/api/jobSearch/v1/jobSearch/marketReportDetails```

Get's the market report details of a noc code

Requires
```
{
  'content': 'noc_code'
}
```

Returns
```
{
  'content': "{
      'wages':[
        {
          'high_wage': '62.50',
          'average_wage': '35.90',
          'low_wage': '20.77',
          'area': 'province name'
        }
      ],
      'education_programs': [
        {
          'title': 'name of job',
          'link': 'link to more details'
        }
      ]
    }"
}
```
- Note: high_wage, average_wage, and low_wage may be ```N/A```

- Example CURL request
  - Request
  ```
  curl -H "Content-Type: application/json" -X POST -d '{"content":"1114"}' localhost:8080/_ah/api/jobSearch/v1/jobSearch/marketReportDetails
  ```
  - Returns
  ```
  {
 "content": "{'education_programs': [{'title': 'Agricultural Business and Management', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=01.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Plant Sciences', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=01.11&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Engineering Physics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=14.12&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Industrial Engineering', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=14.35&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Liberal Arts and Sciences, General Studies and Humanities', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=24.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Botany/Plant Biology', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=26.03&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Microbiological Sciences and Immunology', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=26.05&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Biotechnology', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=26.12&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Mathematics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=27.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Applied Mathematics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=27.03&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Statistics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=27.05&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Multidisciplinary/Interdisciplinary Studies, Other', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=30.99&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Health and Physical Education/Fitness', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=31.05&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Religion/Religious Studies', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=38.02&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Physical Sciences, General', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=40.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Public Administration', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=44.04&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Archeology', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=45.03&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Economics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=45.06&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'International Relations and Affairs', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=45.09&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Political Science and Government', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=45.10&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Business/Commerce, General', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Business Administration, Management and Operations', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.02&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Accounting and Related Services', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.03&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Business/Managerial Economics', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.06&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Finance and Financial Management Services', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.08&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'International Business/Trade/Commerce', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.11&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Management Sciences and Quantitative Methods', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.13&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Marketing', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.14&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Real Estate', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.15&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Taxation', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.16&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'Insurance', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=52.17&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}, {'title': 'History', 'link': '/report_educational-eng.do;jsessionid=A73338C0BD009D3D233CB3217294FA64.imnav74?cip=54.01&area=25565&lang=eng&noc=1114&action=search_occupation_confirm&ln=n&s=3'}], 'wages': [{'area': u'Alberta', 'high_wage': '62.50', 'average_wage': '35.90', 'low_wage': '20.77'}, {'area': u'British Columbia', 'high_wage': '57.69', 'average_wage': '32.31', 'low_wage': '20.19'}, {'area': u'Manitoba', 'high_wage': '51.92', 'average_wage': '28.72', 'low_wage': '18.00'}, {'area': u'New Brunswick', 'high_wage': '46.15', 'average_wage': '25.96', 'low_wage': '17.95'}, {'area': u'Newfoundland and Labrador', 'high_wage': '50.48', 'average_wage': '30.00', 'low_wage': '23.08'}, {'area': u'Northwest Territories', 'high_wage': '57.82', 'average_wage': '43.18', 'low_wage': '20.58'}, {'area': u'Nova Scotia', 'high_wage': '\\nN/A', 'average_wage': '\\nN/A', 'low_wage': '\\nN/A'}, {'area': u'Nunavut', 'high_wage': '\\nN/A', 'average_wage': '\\nN/A', 'low_wage': '\\nN/A'}, {'area': u'Ontario', 'high_wage': '59.34', 'average_wage': '32.78', 'low_wage': '18.00'}, {'area': u'Prince Edward Island', 'high_wage': '\\nN/A', 'average_wage': '\\nN/A', 'low_wage': '\\nN/A'}, {'area': u'Qu\\xe9bec', 'high_wage': '57.69', 'average_wage': '30.00', 'low_wage': '19.74'}, {'area': u'Saskatchewan', 'high_wage': '57.69', 'average_wage': '31.28', 'low_wage': '19.40'}, {'area': u'Yukon', 'high_wage': '\\nN/A', 'average_wage': '\\nN/A', 'low_wage': '\\nN/A'}, {'area': u'Canada', 'high_wage': '57.69', 'average_wage': '31.25', 'low_wage': '19.23'}]}"
  }
  ```
