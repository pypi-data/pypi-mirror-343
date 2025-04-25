import copy
import numpy as np
import ivcensor
if __name__ == '__main__':
    
    def generate_data(n=10000, m=20, p=5, beta_0=0.4, h_2=0.2,eta_A=1, case='case1'):
        random_coefs = np.random.normal(0, 1, size=10*m)
        
        # X = np.zeros((n,p))
        X = np.random.uniform(0, 1, size=(n, p))
        p_Z = [0.25, 0.5, 0.25]
        Z = np.random.choice([0, 1, 2], size=(n, m), p=p_Z)

        gamma = np.sqrt(h_2 / (1.5*m)) * random_coefs[0 : m]
        delta = np.sqrt(h_2 / (1.5*m)) * random_coefs[m : 2*m]

        delta1 = np.sqrt(h_2 / (1.5*m)) * random_coefs[2*m : 3*m]
        delta2 = np.sqrt(h_2 / (1.5*m)) * random_coefs[3*m : 4*m]
        
        epsilon_A = np.random.normal(0, 0.4*(1-h_2), size=n)
        epsilon_Y = np.random.normal(0, 0.4*(1-h_2), size=n)
        U = np.random.normal(0, 0.6*(1-h_2), size=n)

        alpha_case1 = np.zeros(m)
        alpha_case2 = np.sqrt(h_2 / m) * (random_coefs[2*m : 3*m]+0.5)
        alpha_case3 = gamma / 2
        Z_new = copy.deepcopy(Z)
        # Z_new = np.cos(Z*np.pi)
        # Z_new = (Z_new-0.9)**2
        part1 = Z[:, 0] * Z[:, 1]
        part2 = np.exp(Z[:, 2] * Z[:, 3])
        part3 = (Z[:, 4]) * np.sin(Z[:, 0]*np.pi ) 
        part4 = Z[:, 1]*Z[:, 4] * np.cos(Z[:, 2]+ Z[:, 4]*np.pi) 
        
        complex_result = part1 + part2 + part3 + part4
        # Generate alpha based on case
        if case == "case1":
            tmp = np.random.multinomial(1, [1, 0, 0], size=m)
        elif case == "case2":
            tmp = np.random.multinomial(1, [0.6, 0.2, 0.2], size=m)
        elif case == "case3":
            tmp = np.random.multinomial(1, [0.1, 0.9, 0], size=m)
        elif case == "case4":
            tmp = np.random.multinomial(1, [0.1, 0, 0.9], size=m)
        else:
            raise ValueError("Unknown case provided.")

        alpha = tmp[:, 0] * alpha_case1 + tmp[:, 1] * alpha_case2 + tmp[:, 2] * alpha_case3

        # Compute A and Y # np.sqrt(h_2 / (1.5*5)) * complex_result   np.sqrt(h_2 / (1.5*m)) * complex_result + Z_new @ gamma
        A = Z_new @ gamma + U + (1 + Z @ delta)*epsilon_A
        Y = beta_0*A + Z_new @ alpha + np.sum(X,axis=1) - U  + epsilon_Y
       
        return X, Z, A, Y
    def generate_censor_data(n=10000, m=20, p=5, beta_0=0.4, h_2=0.2,eta_A=1,censor_rate=0.4, case='case1'):
        random_coefs = np.random.normal(0, 1, size=10*m)
        
        X = np.random.uniform(-2,2,size=(n,p))
        p_Z = [0.25, 0.5, 0.25]
        # Z = np.random.choice([0, 1, 2], size=(n, m), p=p_Z)
        Z = np.random.uniform(-2,2,size=(n,m))
        # Z = np.random.uniform(0, 2, size=(n, m))
        Z[:,0] = np.cos(np.pi*X[:,0]) + np.random.normal(0, 0.4, size=n)
        Z[:,1] = (X[:,0]+1)*(X[:,1]-1) + np.random.normal(0, 0.4, size=n)
        Z[:,2] = X[:,1]+X[:,0] + np.random.normal(0, 0.4, size=n)
        Z[:,3] = (X[:,1]-0.5)**2 + np.random.normal(0, 0.4, size=n)
        Z[:,4] = np.sin(X[:,1]+X[:,0]) + np.random.normal(0, 0.4, size=n)
        # Z[:,5:10] = np.cos(X[:,0:5]*np.pi) + np.random.normal(0, 0.4, size=(n,5))
        # Z[:,10:15] = np.sin(X[:,0:5]*np.pi) + np.random.normal(0, 0.4, size=(n,5))
        # Z[:,15:20] = (X[:,0:5])**2 + np.random.normal(0, 0.4, size=(n,5))
        gamma = np.sqrt(h_2 / (1.5*m)) * random_coefs[0 : m] 
        delta = np.sqrt(h_2 / (1.5*m)) * random_coefs[m : 2*m]
    
        epsilon_A = np.random.normal(0, 0.4*(1-h_2), size=n)
        epsilon_Y = np.random.normal(0, 0.4*(1-h_2), size=n)
        
    
        alpha_case1 = np.zeros(m)
        alpha_case2 = np.sqrt(h_2 / (1.5*m)) * (random_coefs[2*m : 3*m])/2
        alpha_case3 = gamma / 2
        Z_new = copy.deepcopy(Z)
        Z_new = np.cos(Z*2)
    
        part1 = np.sin((X[:, 0] + X[:, 1])*2+1)
        part2 = np.sin(X[:, 2] + X[:, 3] + X[:, 4]+1)
        part3 = np.sin(X[:, 0]+X[:, 1]+X[:, 2] + X[:, 3] + X[:, 4]+1)
        complex_x1 = np.sin(np.sin(part1+part2)*np.pi+part3)
        complex_x1 = part1
        
        if case == "case1":
            tmp = np.random.multinomial(1, [1, 0, 0], size=m)
        elif case == "case2":
            tmp = np.random.multinomial(1, [0.6, 0.2, 0.2], size=m)
        elif case == "case3":
            tmp = np.random.multinomial(1, [0.1, 0.9, 0], size=m)
        elif case == "case4":
            tmp = np.random.multinomial(1, [0.1, 0, 0.9], size=m)
        else:
            raise ValueError("Unknown case provided.")
        alpha = tmp[:, 0] * alpha_case1 + tmp[:, 1] * alpha_case2 + tmp[:, 2] * alpha_case3
    
        U = np.random.normal(-0.5, 0.6*(1-h_2), size=n)
        A = 2*complex_x1 +  Z_new @ gamma + U + (1 + Z @ delta)*epsilon_A
        T = beta_0*A  + Z_new @ alpha + 0.5*(np.cos(X[:,0]) + X[:,0]*X[:,1]+ np.sin(X[:,2]+X[:,3]+X[:,4]-1))-U  + epsilon_Y 
    
        rr = 0
        
        while True:
            C = np.random.uniform( -1+rr,5+rr, size=n)
            censor_delta = np.where(T <= C, 1, 0) 
            if np.mean(1-censor_delta) >=censor_rate+0.03:
                rr = rr + 0.1
            elif np.mean(1-censor_delta)<=censor_rate-0.03:
                rr = rr - 0.1
            else:
                 break
                
        Y = np.minimum(T,C)
    
        return X, Z, A, Y, censor_delta
    results=[]
    for i in range(1):
        np.random.seed(i)
        X, Z, A, Y, censor_delta= generate_censor_data(n=10000)
        results.append(ivcensor.genius_censor(X, Z, A, Y,censor_delta, model_types=['neural_network','linear_regression','random_forest','xgboost'],
                                    rho_function_names=['ET','EL','CUE']))
    # for i in range(1):
    #     np.random.seed(i)
    #     X, Z, A, Y = generate_data(n=100000)
    #     results.append(ivcensor.genius_noncensor(X, Z, A, Y, model_types=['neural_network','linear_regression','random_forest','xgboost'],
    #                                 rho_function_names=['ET','EL','CUE']))