<?php

define('DB_HOST', '127.0.0.1');
define('DB_PORT', 3306);
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'zomato');


function connect() {
  $link = mysql_connect( DB_HOST.':'.DB_PORT , DB_USER, DB_PASS ) ;
  if (!$link) {     
    die('<br/><br/>Could not connect to the database: <b>' . mysql_error()).'</b>';
    exit;
  }
  mysql_select_db( DB_NAME , $link );
  return $link ;
}


function check($result) {
  if(!$result) {
    print '<b><br/><br/> Sorry , We are facing some problem with the database connectivity. Please return after some time.<br/> Thank You. </b>'.mysql_error();
    exit ;
   } else {
    return true;
   }
}

?>
