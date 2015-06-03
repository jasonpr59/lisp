(define print-and-double
  (lambda (x)
    (print! x)
    (* 2 x)))
(print-and-double 5)

(define (print-and-triple x)
  (print! x)
  (* 3 x))
(print-and-triple 15)
