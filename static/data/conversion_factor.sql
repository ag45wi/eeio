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
-- Table structure for table `conversion_factor`
--

CREATE TABLE `conversion_factor` (
  `id` varchar(45) NOT NULL,
  `energy_type` varchar(45) NOT NULL,
  `unit` varchar(25) NOT NULL,
  `multiplier_factor` float NOT NULL,
  `note` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `conversion_factor`
--

INSERT INTO `conversion_factor` (`id`, `energy_type`, `unit`, `multiplier_factor`, `note`) VALUES
('COAL', 'Coal', 'Ton', 4.2, 'Kalimantan Coal'),
('ELEC', 'Electricity', 'MWh', 0.613, 'Electric Power'),
('FUEL', 'Fuel', 'Kilo Liter', 6.9612, 'FO'),
('NATG', 'Natural Gas', 'MMBTU', 0.1796, 'LNG');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `conversion_factor`
--
ALTER TABLE `conversion_factor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
