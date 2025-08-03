-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 03, 2025 at 10:37 AM
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
-- Table structure for table `co2_factor`
--

CREATE TABLE `co2_factor` (
  `energy_type` varchar(45) NOT NULL,
  `heat_content_hhv` float DEFAULT NULL,
  `emission_factor` float DEFAULT NULL,
  `multiplier` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `co2_factor`
--

INSERT INTO `co2_factor` (`energy_type`, `heat_content_hhv`, `emission_factor`, `multiplier`) VALUES
('Coal', 19.9, 90.3, NULL),
('Electricity', 0.877, NULL, NULL),
('Fuel', 38.65, 68.6, NULL),
('Natural Gas', 37.3, 50, 26.8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `co2_factor`
--
ALTER TABLE `co2_factor`
  ADD PRIMARY KEY (`energy_type`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
