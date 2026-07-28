-- Sample data for DimCustomer
INSERT INTO public."DimCustomer" (customerid, category, country, industry) VALUES
(1, 'Individual', 'US', 'Technology'),
(2, 'Company', 'US', 'Finance'),
(3, 'Individual', 'UK', 'Healthcare'),
(4, 'Company', 'Germany', 'Manufacturing'),
(5, 'Individual', 'Canada', 'Education'),
(6, 'Company', 'France', 'Retail'),
(7, 'Individual', 'Japan', 'Technology'),
(8, 'Company', 'Australia', 'Mining'),
(9, 'Individual', 'Brazil', 'Agriculture'),
(10, 'Company', 'India', 'IT Services');

-- Sample data for DimMonth
INSERT INTO public."DimMonth" (monthid, year, month, monthname, quarter, quartername) VALUES
(1, 2023, 1, 'January', 1, 'Q1'),
(2, 2023, 2, 'February', 1, 'Q1'),
(3, 2023, 3, 'March', 1, 'Q1'),
(4, 2023, 4, 'April', 2, 'Q2'),
(5, 2023, 5, 'May', 2, 'Q2'),
(6, 2023, 6, 'June', 2, 'Q2'),
(7, 2023, 7, 'July', 3, 'Q3'),
(8, 2023, 8, 'August', 3, 'Q3'),
(9, 2023, 9, 'September', 3, 'Q3'),
(10, 2023, 10, 'October', 4, 'Q4'),
(11, 2023, 11, 'November', 4, 'Q4'),
(12, 2023, 12, 'December', 4, 'Q4');

-- Sample data for FactBilling
INSERT INTO public."FactBilling" (rowid, customerid, monthid, billedamount) VALUES
(1, 1, 1, 5000),
(2, 2, 1, 15000),
(3, 3, 1, 3500),
(4, 1, 2, 5200),
(5, 2, 2, 14500),
(6, 4, 2, 22000),
(7, 5, 3, 2800),
(8, 6, 3, 18000),
(9, 1, 3, 5500),
(10, 7, 4, 8000),
(11, 8, 4, 35000),
(12, 9, 4, 1200),
(13, 10, 5, 45000),
(14, 1, 5, 5800),
(15, 2, 5, 16000),
(16, 3, 6, 4000),
(17, 4, 6, 21000),
(18, 5, 6, 3200),
(19, 6, 7, 19500),
(20, 7, 7, 8500),
(21, 8, 7, 38000),
(22, 9, 8, 1500),
(23, 10, 8, 48000),
(24, 1, 8, 6000);
