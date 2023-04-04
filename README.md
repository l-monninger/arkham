# arkham
You can find the site here:
[https://l-monninger-arkham.netlify.app/](https://l-monninger-arkham.netlify.app/). Viewing all requested columns in the table will likely require side-scrolling.

**NOTE**: as of 04/04 websocket connections to Alchemy using the provided token are returning a `403` error code. This was first reported in container health checks on 04/02.

## Runnning locally
To run locally, you will need to run the SPA at `fronts/web` and the blocks service at `services/blocks`.

### `fronts/web`
Once you have installed the required modules, specify the `VITE_BLOCKS_SOCKET` environment variable, pointing it at the domain, port, and path of your websocket. You can do this with a `.env` file if you like. Then you can start the client. 
```
yarn dev
```

### `services/blocks`
Once you have installed the required packages and configured your environment...
```
python run.py
```
You may specif the port with `PORT` environment variable.

## Responses
### 1. How does your solution work?
#### Backend
A single FastAPI (Python) server listens to new blocks from a single async iterator. These blocks are broadcast amongst connected websocket clients. 

When a client first connects, the last five blocks will be sent to it from an in-memory buffer. 

The concurrency model is based entirely on coroutines. 

The backend is deployed as a container on Cloud Run.

#### Frontend
SPA is served using Netlify. A buffer is used to limit display to 5 blocks at a time, placing a relatively low ceiling on memory input.

### 2. How many hours did this take you?
Eight hours across three days.
- +1 hour understanding the API and thinking.
- +1 hour building toy examples.
- +2 hours building broadcasting and debugging.
- +2 hours fiddling with infrastructure that was not used.
- +1 hour fiddling with infrastrucutre that was used.
- +30 minutes on the frontend.
- +30 minutes on the writeup.

### 3. What went well? What went poorly?
#### Well
1. The broadcast design works well, limiting API connections and generally appearing quite scalable in limited testing.
2. The concurrency model (coroutines) seems to do well, and outperformed multiprocessing and multithreading (ofc because it's python) in testing.
3. Frontend was quick to implement.

#### Poorly
1. I may have overdone the software design on the backend; the whole backend could have easily been a single file. At the same time, however, I do actually prefer working with this kind of separation of concerns--even from an early stage.
2. I originally wanted to try and showcase a new stack for which I'd been working on some tooling. This was not at all used and rather costly, particularly for infrastructure.
3. Infrastucture as code efforts were abandoned.
4. Doing this on vacation was not ideal.

#### 4. What did you have trouble with?
1. Debugging infra for whatever reason was trickier than usual. Likely this was because of my environment.
2. I played with a few different concurrency models on the backend and overlooked some silly things that I lost time debuggin.
3. **NEW**: over long runtimes, there appeared to a be starvation issue with the API websocket connection. I fixed this by adjusting my concurrency model slighly and implementing a faster initial reader.

### 5. What would you add to your solution if you had more time?
1. Figure out how to do it faster.
2. Tests and better consideration for edge cases.
3. Observability.
4. Whatever my EM or PM tells me to work on.
5. I probably would work on something else altogether.
6. I might have used the stack I wanted to flex. 
7. A distributed approach.
8. Infrastructure as Code.
9. I'd pay a designer to give me a skeleton for a better frontend.


