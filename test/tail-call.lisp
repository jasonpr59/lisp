(define (count n)
  (print! n)
  (if (< n 10000)
      (count (+ n 1))
    n))
(count 0)

(define (count-a n)
  (if (< n 20000)
      (count-b (+ n 1))
    n))
(define (count-b n)
  (print! n)
  (count-a (+ n 1)))
(count-a 0)
