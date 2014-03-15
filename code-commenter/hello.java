import android.app.Activity;
import android.os.Bundle;

public class hello extends Activity {
	
   /** Called when activity is first created */ 
    @Override
    public void onCreate(Bundle savedInstanceState) {
		
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
		
		final Button btn = (Button) findViewById(R.id.btn);
    }
}


