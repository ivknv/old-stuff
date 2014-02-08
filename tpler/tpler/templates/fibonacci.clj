( defn fibonacci [n] 
	( if ( < n 3 ) n ( + ( fibonacci ( - n 1 ) ) ( fibonacci ( - n 2 ) ) ) )
)
