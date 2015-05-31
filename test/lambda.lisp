(define hypo-squared
 (lambda (s1 s2)
  (+ (square s1) (square s2))))

(define square
 (lambda (x)
  (* x x)))

(hypo-squared 5 12)
