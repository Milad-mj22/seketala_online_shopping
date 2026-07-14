<?php

	$ResCode 		= (isset($_POST['ResCode']) && $_POST['ResCode'] != "") ? $_POST['ResCode'] : "";


	$orderId 				= (isset($_POST['SaleOrderId']) && $_POST['SaleOrderId'] != "") ? $_POST['SaleOrderId'] : "";
	$verifySaleOrderId 		= (isset($_POST['SaleOrderId']) && $_POST['SaleOrderId'] != "") ? $_POST['SaleOrderId'] : "";
	$verifySaleReferenceId 	= (isset($_POST['SaleReferenceId']) && $_POST['SaleReferenceId'] != "") ? $_POST['SaleReferenceId'] : "";
	

echo "<script>window.open('http://foodsoftonline.ir/py_behp_vrfy.php?f1=".$ResCode."&f2=".$orderId."&f3=".$verifySaleReferenceId."&f4=".md5("MnuyyytAAAmnd77++".$orderId)."' ,'_self');</script>";







?>
