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
-- Table structure for table `fec_byyear`
--

CREATE TABLE `fec_byyear` (
  `year` int(11) NOT NULL,
  `energy_type` varchar(45) NOT NULL,
  `fec_val` float NOT NULL,
  `note` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `fec_byyear`
--

INSERT INTO `fec_byyear` (`year`, `energy_type`, `fec_val`, `note`) VALUES
(2016, '01', 63504, '01 - Coal'),
(2016, '02', 329094, '02 - Fuel'),
(2016, '03', 77434, '03 - Natural Gas'),
(2016, '04', 132411, '04 - Electricity'),
(2020, '01', 113416, '01 - Coal'),
(2020, '02', 222339, '02 - Fuel'),
(2020, '03', 97476, '03 - Natural Gas'),
(2020, '04', 159121, '04 - Electricity');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fec_byyear`
--
ALTER TABLE `fec_byyear`
  ADD PRIMARY KEY (`year`,`energy_type`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
