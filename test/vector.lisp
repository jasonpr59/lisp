(define vec (vector 1 3 6 10))
(print! vec)
(print! (vector-ref vec 2))
(vector-set! vec 2 111)
(print! vec)
(print! (vector-length vec))

(define vec2 (make-vector 5))
(print! vec2)

(define vec3 (make-vector 5 1000))
(print! vec3)
(vector-fill! vec3 99)
(print! vec3)
