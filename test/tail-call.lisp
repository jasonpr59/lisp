(define count
  (lambda (n)
     (print! n)
     (if (< n 10000)
	 (count (+ n 1))
       n)))

(count 0)

(define count-a
  (lambda (n)
    (if (< n 20000)
	(count-b (+ n 1))
      n)))

(define count-b
  (lambda (n)
     (print! n)
     (count-a (+ n 1))))

(count-a 0)
