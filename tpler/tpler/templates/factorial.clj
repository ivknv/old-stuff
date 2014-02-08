( defn factorial [n] 
	( if ( < n 3 ) n ( * n ( factorial ( - n 1 ) ) ) )
)
