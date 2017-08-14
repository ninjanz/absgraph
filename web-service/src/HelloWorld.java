import askpapis.ParserServ;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.core.MediaType;

/**
 * Created by ninjanz on 11/07/2017.
 */
@Path("/helloworld")
public class HelloWorld {

    @Path("/abstract")
    @POST
    @Consumes(MediaType.TEXT_PLAIN)
    public String getAbstractJson(String inputJSON) {
        ParserServ asp = new ParserServ();
        asp.setKBInput(inputJSON);

        return asp.getJsonAbstract();
    }

    @Path("/evaluate")
    @POST
    @Consumes(MediaType.TEXT_PLAIN)
    public String evaluateJson(String inputJSON) {
        ParserServ asp = new ParserServ();
        asp.setKBInput(inputJSON);

        return asp.getJsonEvaluateExt();
    }

    @Path("/online-status")
    @GET
    public String getOnlineStatus() {
        return "Online";
    }
}
