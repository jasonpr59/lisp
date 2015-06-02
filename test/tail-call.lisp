(define count
  (lambda (n)
    (begin
     (print! n)
     (if (< n 10000)
	 (count (+ n 1))
       n))))

(count 0)

(define count-a
  (lambda (n)
    (if (< n 20000)
	(count-b (+ n 1))
      n)))

(define count-b
  (lambda (n)
    (begin
     (print! n)
     (count-a (+ n 1)))))

(count-a 0)
