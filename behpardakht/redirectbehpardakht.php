<?php
$Authority=$_REQUEST["auth"];
$token=$_REQUEST["token"];
$hash=$_REQUEST["hsh"];

if($hash!=md5($token.$Authority."GHUdjjjsSfg89++tytr"))
{
   	    echo("<div style='width:500px;margin:auto;color:black;background-color:red;font-size:22px;margin-top:80px;pading-top:30px;text-align:center;color:white;height:50px;'>درانتقال به درگاه پرداخت مشکلی بوجود آمد-5001</div>");
    	echo(str_replace('','"',"<div style='width:200px;margin:auto;'> <button type='button' style='width:200px;height:50px;margin-top:20px;' onclick='window.history.go(-2); return false;'>بازگشت</button></div>")); 
		exit();


}


			echo "<form name='myform' action='https://bpm.shaparak.ir/pgwchannel/startpay.mellat' method='POST'><input type='hidden' id='RefId' name='RefId' value='{$Authority}'></form><script type='text/javascript'>window.onload = formSubmit; function formSubmit() { document.forms[0].submit(); }</script>";


?>
