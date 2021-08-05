
# KPI builder


Steps on what needs to happen:
Start from scratch, use this as a good template for what to do 
to get stock info 


Major steps:
1. Set up dash

2. Input box with stock ticker
    - Look at good stuff for this 
    - For v1 just make sure this loads 

3. Input box with selected industry 
    - Look in folder for list of companies in this industry 
    - Pull down GROWTH average. Will need to look at CapIQ for this bit. Includes industry PLUS this stock ticker 
4. User inputs stock ticker, API call 
    - 

5. Input time. At this point, add deviation 
    - Stock price for client grows (ideally) in red
    - Industry growth continues in black line (but minus) client 

6. Build simple test suite 
    Industry = Shoes: Nike, Timberland, Adidas, Asics
    Company: Timberland. 
    Pinpoint: Launch June 23, 2021  

    Expectations:
        - Industry loads
            - Industry list exists in folder 
            - All tickers on list exist 
        - Starting point is a time that exists (last 5 years max). Can't be in the future
        - Stock ticker exists 

7. Jenkins for CI/ CD


Notes:
1. Add "request an industry" feature. Sends me an email
when people need to add a new subsection. Expect 1-2 weeks. 
Ping directly if need more urgently. 



