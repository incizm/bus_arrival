ArriveLah
===

Fast simple API for bus arrival times in Singapore.

This is like a proxy to [LTA's DataMall Bus Arrival API](http://www.mytransport.sg/content/mytransport/home/dataMall.html).

Development
---

1. Request API access and add API account key(https://datamall.lta.gov.sg/content/datamall/en/request-for-api.html).
    1. Copy and rename `.env.example` to `.env`. Edit the file.
    2. Add environment variables.
2. Install [Vercel CLI](https://vercel.com/docs/cli).
3. `npm install`
4. `npm start`
5. `python viewer.py`

License
---

[MIT](http://cheeaun.mit-license.org/). Data is copyrighted by [LTA](http://www.mytransport.sg/).
