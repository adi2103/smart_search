```
❯ curl http://localhost:8000/health
{"status":"healthy"}%                                         
❯ curl -X POST http://localhost:8000/clients/1/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Doc", "content": "Investment portfolio analysis for retirement planning"}'
{"id":3,"client_id":1,"title":"Test Doc","content":"Investment portfolio analysis for retirement planning","summary":"Investment portfolio analysis for retirement planning","created_at":"2025-09-16T22:27:32.752760Z"}%                               
❯ curl -X POST http://localhost:8000/clients/1/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "Client meeting about asset allocation and risk tolerance"}'
{"id":3,"client_id":1,"content":"Client meeting about asset allocation and risk tolerance","summary":"Client meeting about asset allocation and risk tolerance","created_at":"2025-09-16T22:28:26.933630Z"}%                                            
❯ curl -G http://localhost:8000/search --data-urlencode "q=investment" --data-urlencode "type=document"
{"query":"investment","type":"document","results":[{"id":1,"type":"document","client_id":1,"title":"Investment Portfolio Analysis 2024","content":"This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.","summary":"This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.","created_at":"2025-09-16T21:37:21.038096Z","score":0.01639344262295082},{"id":2,"type":"document","client_id":1,"title":"Test Document 2","content":"This is a test document about financial planning and investment strategies for retirement.","summary":"This is a test document about financial planning and investment strategies for retirement.","created_at":"2025-09-16T21:38:32.741390Z","score":0.016129032258064516},{"id":3,"type":"document","client_id":1,"title":"Test Doc","content":"Investment portfolio analysis for retirement planning","summary":"Investment portfolio analysis for retirement planning","created_at":"2025-09-16T22:27:32.752760Z","score":0.015873015873015872}]}%         
❯ curl -G http://localhost:8000/search --data-urlencode "q=investment" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-  0     0    0     0    0     0      0      0 --:--:-- --:--:-  0     0    0     0    0     0      0      0 --:--:--  0:00:0100  1416  100  1416    0     0    674      0  0:00:02  0:00:0100  1416  100  1416    0     0    674      0  0:00:02  0:00:02 --:--:--   673
{
  "query": "investment",
  "type": "document",
  "results": [
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.01639344262295082
    },
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.016129032258064516
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.015873015873015872
    }
  ]
}
 ~/c/project_20250915_2114_smart_search  main !1                                     ✔  23:3
 ~/c/project_20250915_2114_smart_search  main !1                                   ✔  23:30:
 ~/c/project_20250915_2114_smart_search  main !1                                 ✔  23:30:50
 ~/c/project_20250915_2114_smart_search  main !1                                         ✔ 
 ~/c/project_20250915_2114_smart_search  main !1                                        ✔  
 ~/c/project_20250915_2114_smart_search  main !1                                ✔  23:30:50
❯ curl -G http://localhost:8000/search --data-urlencode "q=independence" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2903  100  2903    0     0   2103      0  0:00:01  0:00:01 --:--:--  2102
{
  "query": "independence",
  "type": "document",
  "results": [
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.01639344262295082
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.016129032258064516
    },
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.015873015873015872
    },
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.015625
    }
  ]
}
❯ curl -G http://localhost:8000/search --data-urlencode "q=maths" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2896  100  2896    0     0   1934      0  0:00:01  0:00:01 --:--:--  1934
{
  "query": "maths",
  "type": "document",
  "results": [
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.01639344262295082
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.016129032258064516
    },
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.015873015873015872
    },
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.015625
    }
  ]
}
❯ curl -G http://localhost:8000/search --data-urlencode "q=US" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2893  100  2893    0     0   2141      0  0:00:01  0:00:01 --:--:--  2141
{
  "query": "US",
  "type": "document",
  "results": [
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.01639344262295082
    },
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.016129032258064516
    },
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.015873015873015872
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.015625
    }
  ]
}
❯ curl -G http://localhost:8000/search --data-urlencode "q=offensive" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2900  100  2900    0     0   2091      0  0:00:01  0:00:01 --:--:--  2092
{
  "query": "offensive",
  "type": "document",
  "results": [
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.01639344262295082
    },
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.016129032258064516
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.015873015873015872
    },
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.015625
    }
  ]
}
❯ curl -G http://localhost:8000/search --data-urlencode "q=yield" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2896  100  2896    0     0   2013      0  0:00:01  0:00:01 --:--:--  2012
{
  "query": "yield",
  "type": "document",
  "results": [
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.01639344262295082
    },
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.016129032258064516
    },
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.015873015873015872
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.015625
    }
  ]
}
❯ curl -G http://localhost:8000/search --data-urlencode "q=2024" --data-urlencode "type=document" | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2895  100  2895    0     0   2074      0  0:00:01  0:00:01 --:--:--  2075
{
  "query": "2024",
  "type": "document",
  "results": [
    {
      "id": 1,
      "type": "document",
      "client_id": 1,
      "title": "Investment Portfolio Analysis 2024",
      "content": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "summary": "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management.",
      "created_at": "2025-09-16T21:37:21.038096Z",
      "score": 0.03278688524590164
    },
    {
      "id": 2,
      "type": "document",
      "client_id": 1,
      "title": "Test Document 2",
      "content": "This is a test document about financial planning and investment strategies for retirement.",
      "summary": "This is a test document about financial planning and investment strategies for retirement.",
      "created_at": "2025-09-16T21:38:32.741390Z",
      "score": 0.016129032258064516
    },
    {
      "id": 3,
      "type": "document",
      "client_id": 1,
      "title": "Test Doc",
      "content": "Investment portfolio analysis for retirement planning",
      "summary": "Investment portfolio analysis for retirement planning",
      "created_at": "2025-09-16T22:27:32.752760Z",
      "score": 0.015873015873015872
    },
    {
      "id": 4,
      "type": "document",
      "client_id": 1,
      "title": "Comprehensive Investment Strategy Report",
      "content": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns. Our analysis suggests a defensive positioning with increased allocation to government bonds and dividend-paying stocks. The technology sector shows mixed signals with some companies demonstrating strong fundamentals while others face regulatory challenges. Emerging markets present both opportunities and risks, requiring careful selection and diversification. Risk management strategies should include regular rebalancing and stress testing of portfolio positions. Long-term investors should focus on quality companies with sustainable competitive advantages and strong balance sheets.",
      "summary": "This comprehensive investment strategy report analyzes the current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, real estate, and alternative investments. Market volatility has increased significantly due to geopolitical tensions and inflation concerns.",
      "created_at": "2025-09-16T22:34:26.134256Z",
      "score": 0.015625
    }
  ]
}
```