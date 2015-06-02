(define count
  (lambda (n)
    (begin
     (print! n)
     (count (+ n 1)))))

(count 0)
