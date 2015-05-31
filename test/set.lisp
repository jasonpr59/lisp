(define counter 0)

(define inc
  (lambda ()
    (set! counter (+ counter 1))))

(inc)
(inc)
(inc)
(print! counter)
