(define counter
  (lambda (init)
    (begin
     (define count init)
     (lambda ()
       (begin
	(set! count (+ count 1))
	count)))))

(define ctr (counter 5))

(ctr)
(ctr)
