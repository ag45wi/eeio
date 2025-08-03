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
-- Table structure for table `sector_agg`
--

CREATE TABLE `sector_agg` (
  `id` varchar(6) NOT NULL,
  `name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `sector_agg`
--

INSERT INTO `sector_agg` (`id`, `name`) VALUES
('01', 'Energy'),
('02', 'Agriculture '),
('03', 'Wood and forest products'),
('04', 'Fisheries'),
('05', 'Mining '),
('06', 'Food, beverage and food processing '),
('07', 'Chemical industries '),
('08', 'Metal and heavy industries '),
('09', 'Building, road and constructions'),
('10', 'Textiles '),
('11', 'Electronics '),
('12', 'Transportation'),
('13', 'Services '),
('14', 'Others');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sector_agg`
--
ALTER TABLE `sector_agg`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
