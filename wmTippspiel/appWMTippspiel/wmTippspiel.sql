-- phpMyAdmin SQL Dump
-- version 3.3.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 26. Mai 2010 um 21:39
-- Server Version: 5.1.37
-- PHP-Version: 5.2.10-2ubuntu6.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `wmTippspiel`
--

--
-- Daten für Tabelle `appWMTippspiel_begegnung`
--

INSERT INTO `appWMTippspiel_begegnung` (`id`, `mannschaftHeim_id`, `mannschaftGast_id`, `toreHeim`, `toreGast`, `datum`, `art`) VALUES
(1, 2, 1, 3, 5, '2010-05-10 20:15:00', 'Gruppe A'),
(2, 1, 3, 0, 0, '2010-06-17 11:11:46', 'Gruppe A'),
(3, 2, 3, 0, 0, '2010-06-10 17:01:25', 'Gruppe A'),
(4, 4, 1, 0, 0, '2010-05-22 17:12:09', 'Gruppe A'),
(6, 4, 5, 0, 0, '2010-06-23 13:19:58', 'Gruppe A');

--
-- Daten für Tabelle `appWMTippspiel_mannschaft`
--

INSERT INTO `appWMTippspiel_mannschaft` (`id`, `name`) VALUES
(1, 'Deutschland'),
(2, 'Frankreich'),
(3, 'England'),
(4, 'Portugal'),
(5, 'Chile');

--
-- Daten für Tabelle `appWMTippspiel_tipps`
--

INSERT INTO `appWMTippspiel_tipps` (`id`, `user_id`, `begegnung_id`, `toreHeim`, `toreGast`, `tippDatum`) VALUES
(32, 2, 3, 33, 66, '2010-05-21 17:54:00'),
(33, 2, 1, 5, 6, '2010-05-23 18:59:00'),
(31, 2, 4, 0, 0, '2010-05-21 17:46:00'),
(30, 2, 2, 0, 0, '2010-05-21 17:55:00'),
(34, 2, 6, 0, 0, '2010-05-23 16:38:00'),
(35, 1, 1, 4, 6, '2010-05-23 10:15:55');
