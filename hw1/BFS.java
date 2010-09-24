import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class BFS extends Configured implements Tool
{  
  static class BFSMapper extends Mapper<LongWritable, Text, IntWritable, Text>
  {
	  private IntWritable num = new IntWritable();
	  private Text word = new Text();
	  
	  public void map(LongWritable key, Text value, Context context) throws IOException,
	  InterruptedException
	  {
		  //split string up into components (after removing whitespace)
		  String line = value.toString().trim();
		  String[] keyVal = line.split("[|]");
		  
		  //set components to (node #, distance #, outlink #'s)
		  String node = keyVal[0];
		  String smallest_distance = keyVal[1];
		  String link_string = "";
		  String[] links = null;
		  
		  if(keyVal.length > 2)
		  {
			  //loop through outlinks
			  link_string = keyVal[2];
			  links = keyVal[2].split(";");
			  
			  int distance = Integer.parseInt(smallest_distance);
			  
			  //only increment if not infinity (int max)
			  if(!smallest_distance.equalsIgnoreCase("2147483647"))
				  distance++;
			  
			  //output (outlink, distance) pairs
			  for(int i = 0; i < links.length; i++)
			  {
				  num.set(Integer.parseInt(links[i]));
				  word.set(Integer.toString(distance) + "|");
				  context.write(num, word);
			  }
		  }
		  
		  //finally output original outlink list triplet
		  num.set(Integer.parseInt(node));
		  word.set(smallest_distance + "|" + link_string);
		  context.write(num, word);
	  }
  }
  
  static class BFSReducer extends Reducer<IntWritable, Text, Text, Text>
  {
	private Text blank = new Text("");
	private Text word = new Text();
	
    public void reduce(IntWritable key, Iterable<Text> values, Context context)
    throws IOException, InterruptedException
    {
    	int min_dist = Integer.MAX_VALUE;
    	String link_string = "";
    	
    	//cycle through all values to compute new minimum distance
    	for(Text value : values)
    	{
    		//one of the values will contain the original outlinks.
    		//save for output.
    		String[] val_list = value.toString().split("[|]");
    		if(val_list.length > 1)
    			link_string = val_list[1];
    		
    		int dist = Integer.parseInt(val_list[0]);
    		min_dist = Math.min(dist, min_dist);
    	}
    	
    	//set output back to original, after computing new min_dist
    	word.set(key.toString() + "|" + Integer.toString(min_dist) + "|" + link_string);
    	context.write(blank, word);
    }
  }
  
  public int run(String[] args) throws Exception
  {
	  if (args.length != 2)
	  {
		  System.err.printf("Usage: %s [generic options] <input> <output>\n", getClass().getSimpleName());
		  ToolRunner.printGenericCommandUsage(System.err);
		  return -1;
	  }
	  
      // Configuration processed by ToolRunner
      Configuration conf = getConf();
      
      // Create a JobConf using the processed conf
      Job job = new Job(conf, getClass().getSimpleName());
      
      // Process custom command-line options
      Path in = new Path(args[0]);
      Path out = new Path(args[1]);
      
      // Specify various job-specific parameters
      FileInputFormat.addInputPath(job, in);
      FileOutputFormat.setOutputPath(job, out);
      job.setMapperClass(BFSMapper.class);
      job.setReducerClass(BFSReducer.class);
      
      job.setJarByClass(BFS.class);

      job.setOutputValueClass(Text.class);
      job.setOutputKeyClass(IntWritable.class);
      
      return (job.waitForCompletion(true) ? 0 : 1);
    }
    
    public static void main(String[] args) throws Exception
    {
      int res = ToolRunner.run(new BFS(), args);
      System.exit(res);
    }
}