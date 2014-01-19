int fibonacci(int n) {
	return n>2 ? fibonacci(n-2)+fibonacci(n-1) : n;
}