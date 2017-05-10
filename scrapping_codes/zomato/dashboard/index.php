<?php

//including the database authentication functions and variables
include_once('./library/database.php');

//connecting to database
$link = connect();

$queries = array(
	"country_count" => "SELECT COUNT(*) FROM `country`",
	"city_count" => "SELECT COUNT(*) FROM `city`",
	"listing_count" => "SELECT COUNT(*) FROM `listing`",
	"restaurant_count" => "SELECT COUNT(*) FROM `restaurant`",
	"crawled_city_count" => "SELECT COUNT(*) FROM `city` where `finished` = 1",
	"total_pages_count" => "SELECT SUM(pages) FROM `city`",
	"crawled_pages_count" => "SELECT SUM(pages_crawled) FROM `city`"
);

$q_res = array();

foreach ($queries as $query_name => $query) {
	$result = mysql_query($query);
	if(check($result)) {
		$q_res[$query_name] = mysql_fetch_row($result)[0];
	} else{
		$q_res[$query_name] = 0;
	}
}

$page = file_get_contents('index.html');
$page = str_replace('{country_count}', $q_res["country_count"], $page);
$page = str_replace('{city_count}', $q_res["city_count"], $page);
$page = str_replace('{listing_count}', $q_res["listing_count"], $page);
$page = str_replace('{crawled_city_count}', $q_res["crawled_city_count"], $page);

$cities_crawled_percentage = round(($q_res["crawled_city_count"]/$q_res["city_count"])*100, 2);
$listings_pages_percentage = round(($q_res["crawled_pages_count"]/$q_res["total_pages_count"])*100, 2);
$restaurants_percentage = round(($q_res["restaurant_count"]/$q_res["listing_count"])*100, 2);

$page = str_replace('{cities_crawled_percentage}', $cities_crawled_percentage, $page);
$page = str_replace('{listings_pages_percentage}', $listings_pages_percentage, $page);
$page = str_replace('{restaurants_percentage}', $restaurants_percentage, $page);


echo $page;

?>