-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 03, 2025 at 10:38 AM
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
-- Table structure for table `energy_lst`
--

CREATE TABLE `energy_lst` (
  `energy_type_code` varchar(3) NOT NULL,
  `energy_type_name` varchar(45) DEFAULT NULL,
  `name_short` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `energy_lst`
--

INSERT INTO `energy_lst` (`energy_type_code`, `energy_type_name`, `name_short`) VALUES
('01', 'Coal', 'COAL'),
('02', 'Fuel', 'FUEL'),
('03', 'Natural Gas', 'NATU'),
('04', 'Electricity', 'ELEC');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `energy_lst`
--
ALTER TABLE `energy_lst`
  ADD PRIMARY KEY (`energy_type_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
