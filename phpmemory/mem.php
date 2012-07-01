<?
	class a {
		private $text = "aklsdfjaklsdfjlaksdjfaklsdfj";
		private $b;
		public function set_b($b) { $this->b = $b; }
	}

	for($i=0;$i<100000;$i++) {
		$a = new a();
		$b = new a();
		$a->set_b($b);
		$b->set_b($a);
	}
	print memory_get_usage(true) . "\n";
	
?>
