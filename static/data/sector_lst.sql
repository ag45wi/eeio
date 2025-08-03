-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 03, 2025 at 10:39 AM
-- Server version: 10.6.22-MariaDB-cll-lve
-- PHP Version: 8.3.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inovasi9_db_eeio`
--

-- --------------------------------------------------------

--
-- Table structure for table `sector_lst`
--

CREATE TABLE `sector_lst` (
  `sector_agg` varchar(64) NOT NULL,
  `sector_code` varchar(4) NOT NULL,
  `sector_name` varchar(128) NOT NULL,
  `sector_label` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `sector_lst`
--

INSERT INTO `sector_lst` (`sector_agg`, `sector_code`, `sector_name`, `sector_label`) VALUES
('02', '001', 'Paddy', 'DET'),
('02', '002', 'Corn', 'DET'),
('02', '003', 'Sweet potato', 'DET'),
('02', '004', 'Cassava', 'DET'),
('02', '005', 'Other tubers', 'DET'),
('02', '006', 'Peanuts', 'DET'),
('02', '007', 'Soybean', 'DET'),
('02', '008', 'Other nuts', 'DET'),
('02', '009', 'Grains and other foodstuffs', 'DET'),
('02', '010', 'Vegetables', 'DET'),
('02', '011', 'Decorative plants', 'DET'),
('02', '012', 'Sugarcane', 'DET'),
('02', '013', 'Tobacco', 'DET'),
('02', '014', 'Fiber plant', 'DET'),
('02', '015', 'Other plantations', 'DET'),
('02', '016', 'Fruits', 'DET'),
('02', '017', 'Biopharmaceutical plants', 'DET'),
('02', '018', 'Rubber', 'DET'),
('02', '019', 'Coconut', 'DET'),
('02', '020', 'Palm oil', 'DET'),
('02', '021', 'Coffee', 'DET'),
('02', '022', 'Tea', 'DET'),
('02', '023', 'Cocoa', 'DET'),
('02', '024', 'Clove', 'DET'),
('02', '025', 'Cashew', 'DET'),
('06', '026', 'Livestock and their products (except fresh milk)', 'DET'),
('06', '027', 'Fresh milk', 'DET'),
('06', '028', 'Poultry and their products ', 'DET'),
('06', '029', 'Other animal care products', 'DET'),
('13', '030', 'Agriculture, forestry and fisheries services', 'DET'),
('03', '031', 'Wood', 'DET'),
('03', '032', 'Other forest products', 'DET'),
('04', '033', 'Fish', 'DET'),
('04', '034', 'Shrimp and other crustaceans', 'DET'),
('04', '035', 'Other aquatic biota', 'DET'),
('04', '036', 'Seaweeds', 'DET'),
('01', '037', 'Coal and lignite', 'DET'),
('01', '038', 'Crude oil', 'DET'),
('01', '039', 'Natural gas and geothermal', 'DET'),
('05', '040', 'Iron sand and iron ore', 'DET'),
('05', '041', 'Tin ore ', 'DET'),
('05', '042', 'Bauxite ore', 'DET'),
('05', '043', 'Copper ore ', 'DET'),
('05', '044', 'Nickel ore', 'DET'),
('05', '045', 'Other metal mining ', 'DET'),
('05', '046', 'Gold ore ', 'DET'),
('05', '047', 'Silver ore ', 'DET'),
('05', '048', 'Minerals', 'DET'),
('05', '049', 'Non-metal minerals', 'DET'),
('05', '050', 'Coarse salt', 'DET'),
('13', '051', 'Petroleum and natural gas mining services ', 'DET'),
('05', '052', 'Other mining and quarrying services ', 'DET'),
('06', '053', 'Slaughterhouse', 'DET'),
('06', '054', 'Meat processing and preservation products', 'DET'),
('06', '055', 'Dried fish and salted fish', 'DET'),
('06', '056', 'Fish processing and preservation products', 'DET'),
('06', '057', 'Fruit and vegetables (processed and preserved) ', 'DET'),
('06', '058', 'Animal and vegetables oil', 'DET'),
('02', '059', 'Copra', 'DET'),
('06', '060', 'Food and drinks from milk', 'DET'),
('06', '061', 'Other flour', 'DET'),
('06', '062', 'Wheat and meslin flour', 'DET'),
('06', '063', 'Rice milling products', 'DET'),
('06', '064', 'Bread, biscuits', 'DET'),
('06', '065', 'Sugar', 'DET'),
('06', '066', 'Chocolate and confectionery', 'DET'),
('06', '067', 'Noodles, macaroni and pasta', 'DET'),
('06', '068', 'Processed coffee', 'DET'),
('06', '069', 'Processed tea', 'DET'),
('06', '070', 'Processed soybean', 'DET'),
('06', '071', 'Other foods', 'DET'),
('06', '072', 'Processed pet food', 'DET'),
('06', '073', 'Alcohol beverages', 'DET'),
('06', '074', 'Non-alcohol beverages', 'DET'),
('06', '075', 'Cigarette', 'DET'),
('06', '076', 'Processed tobacco', 'DET'),
('10', '077', 'Yarn', 'DET'),
('10', '078', 'Textile', 'DET'),
('10', '079', 'Tapestry, rope, and other floor coverings ', 'DET'),
('10', '080', 'Textiles other than fabrics and garments', 'DET'),
('10', '081', 'Knitted products', 'DET'),
('10', '082', 'Apparel', 'DET'),
('10', '083', 'Leather preservation and tanning products', 'DET'),
('10', '084', 'Leather goods', 'DET'),
('10', '085', 'Footwear', 'DET'),
('03', '086', 'Sawn and processed wood', 'DET'),
('03', '087', 'Plywoods', 'DET'),
('03', '088', 'Building materials from wood', 'DET'),
('03', '089', 'Other products of wood, cork, bamboo and rattan', 'DET'),
('03', '090', 'Pulp', 'DET'),
('03', '091', 'Paper', 'DET'),
('03', '092', 'Paper and cardboard', 'DET'),
('14', '093', 'Printing', 'DET'),
('14', '094', 'Other goods from non-metal materials ', 'DET'),
('07', '095', 'Oil and gas refinery products', 'DET'),
('07', '096', 'Basic chemicals (except fertilizer)', 'DET'),
('07', '097', 'Fertilizers', 'DET'),
('07', '098', 'Synthetic resin, plastic material and synthetic fiber ', 'DET'),
('07', '099', 'Pesticide', 'DET'),
('07', '100', 'Paint and printing ink', 'DET'),
('07', '101', 'Varnish and lacquer ', 'DET'),
('07', '102', 'Soap and cleaning agents ', 'DET'),
('07', '103', 'Cosmetics', 'DET'),
('07', '104', 'Other chemicals', 'DET'),
('07', '105', 'Pharmaceuticals', 'DET'),
('14', '106', 'Traditional medicine', 'DET'),
('14', '107', 'Tire ', 'DET'),
('14', '108', 'Crumb and smoked rubber', 'DET'),
('14', '109', 'Other goods from rubber', 'DET'),
('14', '110', 'Plastics items ', 'DET'),
('14', '111', 'Glass and glassware ', 'DET'),
('09', '112', 'Clay, ceramics and porcelain products', 'DET'),
('09', '113', 'Cement ', 'DET'),
('08', '114', 'Iron and steels', 'DET'),
('08', '115', 'Non-ferrous base metals', 'DET'),
('08', '116', 'Metal casting products', 'DET'),
('08', '117', 'Metal building materials ', 'DET'),
('08', '118', 'Weapons and ammunition, metallurgy and metalworking services', 'DET'),
('08', '119', 'Metal kitchen, carpentry, household and office furniture ', 'DET'),
('08', '120', 'Other metal products', 'DET'),
('11', '121', 'Electronics, communication and their equipments', 'DET'),
('14', '122', 'Measuring instruments, photography, optics and clocks', 'DET'),
('11', '123', 'Generators and electric motors', 'DET'),
('11', '124', 'Electrical machines and equipment ', 'DET'),
('11', '125', 'Battery and accumulator', 'DET'),
('11', '126', 'Other electrical equipments', 'DET'),
('11', '127', 'Electrical appliance for household', 'DET'),
('14', '128', 'Starting machine', 'DET'),
('14', '129', 'Machinery for office and accounting purposes, and parts and equipment thereof', 'DET'),
('14', '130', 'Other machines and equipments', 'DET'),
('11', '131', 'Motor vehicles (except motorcycles)', 'DET'),
('13', '132', 'Ships and their repair services', 'DET'),
('13', '133', 'Trains and their repair services', 'DET'),
('13', '134', 'Aircrafts and their repair services ', 'DET'),
('12', '135', 'Other transportations', 'DET'),
('12', '136', 'Motorcycles ', 'DET'),
('14', '137', 'Non-metal home and office furnitures', 'DET'),
('14', '138', 'Jewelry', 'DET'),
('14', '139', 'Musical instruments ', 'DET'),
('14', '140', 'Sports equipment ', 'DET'),
('14', '141', 'Toys and games ', 'DET'),
('14', '142', 'Medical equipments', 'DET'),
('14', '143', 'Other processing industry products', 'DET'),
('13', '144', 'Maintenance and repair services for manufactured metal products, machinery and equipment', 'DET'),
('01', '145', 'Electricity', 'DET'),
('01', '146', 'Products of natural and artificial gas, supply of steam/hot water, cold air and ice products', 'DET'),
('14', '147', 'Water supply', 'DET'),
('14', '148', 'Waste and recycling management ', 'DET'),
('09', '149', 'Residential and non-residential buildings ', 'DET'),
('09', '150', 'Electrical, gas, drinking water and communication buildings and installations', 'DET'),
('09', '151', 'Agricultural infrastructure', 'DET'),
('09', '152', 'Road, bridge and harbor', 'DET'),
('09', '153', 'Other buildings ', 'DET'),
('14', '154', 'Cars and motorcycles trade ', 'DET'),
('13', '155', 'Car and motorcycle repair and maintenance ', 'DET'),
('14', '156', 'Trade other than cars and motorcycles ', 'DET'),
('13', '157', 'Rail transport services ', 'DET'),
('12', '158', 'Land transportation services other than rail transport ', 'DET'),
('12', '159', 'Sea freight services ', 'DET'),
('12', '160', 'River, lake and ferry transport services ', 'DET'),
('12', '161', 'Air freight services ', 'DET'),
('13', '162', 'Transportation support services ', 'DET'),
('13', '163', 'Postal and courier services ', 'DET'),
('13', '164', 'Accommodation services', 'DET'),
('13', '165', 'Food and drink services', 'DET'),
('14', '166', 'Publication', 'DET'),
('13', '167', 'Broadcasting and programming services, film and sound recording ', 'DET'),
('13', '168', 'Telecommunication services ', 'DET'),
('13', '169', 'Computer and information technology consulting services', 'DET'),
('13', '170', 'Banking financial services ', 'DET'),
('13', '171', 'Insurance services ', 'DET'),
('13', '172', 'Pension services ', 'DET'),
('13', '173', 'Other financial institution services ', 'DET'),
('13', '174', 'Real estate services', 'DET'),
('13', '175', 'Professional, scientific and technical services ', 'DET'),
('13', '176', 'Rental and business support services ', 'DET'),
('13', '177', 'General government services ', 'DET'),
('13', '178', 'Government education services ', 'DET'),
('13', '179', 'Government health services ', 'DET'),
('13', '180', 'Other government services ', 'DET'),
('NN', '1800', 'Total Intermediate Demand', 'AGG'),
('13', '181', 'Private education services ', 'DET'),
('13', '182', 'Health services and private social activities ', 'DET'),
('13', '183', 'Arts, entertainment and recreation services ', 'DET'),
('14', '184', 'Repair of other household and personal items ', 'DET'),
('13', '185', 'Other services ', 'DET'),
('NN', '1900', 'Total intermediate consumption', 'AGG'),
('NN', '1950', 'Taxes minus product subsidies', 'AGG'),
('NN', '2000', 'Total import consumption', 'AGG'),
('NN', '2010', 'Compensation of employees', 'AGG'),
('NN', '2020', 'Gross operating surplus', 'AGG'),
('NN', '2030', 'Taxes minus other production subsidies', 'AGG'),
('NN', '2090', 'Gross Value Added', 'AGG'),
('NN', '2100', 'Total Input', 'AGG'),
('NN', '3011', 'Households consumption', 'AGG'),
('NN', '3012', 'Non-profit association households consumption', 'AGG'),
('NN', '3020', 'Government consumption', 'AGG'),
('NN', '3030', 'Gross fixed capital formation', 'AGG'),
('NN', '3040', 'Inventory change', 'AGG'),
('NN', '3050', 'Exports (F.o.b)', 'AGG'),
('NN', '3060', 'Service exports', 'AGG'),
('NN', '3090', 'Total Final Demand', 'AGG'),
('NN', '3100', 'Use based on buyer price', 'AGG'),
('NN', '4010', 'Import (c.i.f)', 'AGG'),
('NN', '4020', 'Service imports', 'AGG'),
('NN', '4030', 'Adjustment (i.f)', 'AGG'),
('NN', '4090', 'Total Import', 'AGG'),
('NN', '5010', 'Big trading margin', 'AGG'),
('NN', '5020', 'Retail trading margin', 'AGG'),
('NN', '5030', 'Freight Cost', 'AGG'),
('NN', '5090', 'Total Trading Margin and Freight Cost', 'AGG'),
('NN', '6090', 'Total Taxes Minus Product Subsidies', 'AGG'),
('NN', '7000', 'Total Domestic Output at Basic Price', 'AGG'),
('NN', '8000', 'Supply based on buyer price', 'AGG'),
('NN', 'i.f', 'Adjustment (i.f)', 'AGG');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sector_lst`
--
ALTER TABLE `sector_lst`
  ADD PRIMARY KEY (`sector_code`),
  ADD UNIQUE KEY `sector_code_UNIQUE` (`sector_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
