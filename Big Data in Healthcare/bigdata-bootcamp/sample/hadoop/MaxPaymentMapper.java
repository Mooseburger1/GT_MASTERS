import java.io.IOException;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
public class MaxPaymentMapper
  extends Mapper<LongWritable, Text, Text, FloatWritable> {
  @Override
  public void map(LongWritable offset, Text lineText, Context context)
      throws IOException, InterruptedException {
    String line = lineText.toString();
    if(line.contains("PAYMENT")) {
        String patientID = line.split(",")[0];
        float payment = Float.parseFloat(line.split(",")[3]);
        context.write(new Text(patientID), new FloatWritable(payment));
    }
  }
}