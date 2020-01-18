import java.io.IOException;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
public class MaxPaymentReducer extends Reducer<Text ,  FloatWritable ,  Text ,  FloatWritable > {
     @Override public void reduce( Text patientID,  Iterable<FloatWritable> payments,  Context context)
         throws IOException,  InterruptedException {
      float maxPayment  = 0.0f;
      for ( FloatWritable payment : payments) {
        float p = payment.get();
        if(p > maxPayment)
          maxPayment = p;
      }
      context.write(patientID,  new FloatWritable(maxPayment));
    }
}